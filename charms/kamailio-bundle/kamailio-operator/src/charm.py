#!/usr/bin/env python3
# Copyright 2021 Gabor Meszaros
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging
from typing import Any, Dict

from charms.nginx_ingress_integrator.v0.ingress import IngressRequires
from ops.charm import ActionEvent, CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import (
    ActiveStatus,
    BlockedStatus,
    Container,
    MaintenanceStatus,
    WaitingStatus,
)
from ops.pebble import ServiceStatus, PathError

logger = logging.getLogger(__name__)


class KamailioCharm(CharmBase):
    """Kamailio Charm Operator."""

    # StoredState is used to store data the charm needs persisted across invocations.
    _stored = StoredState()

    def __init__(self, *args) -> None:
        super().__init__(*args)

        # Observe charm events
        event_observer_mapping = {
            self.on.kamailio_pebble_ready: self._on_config_changed,
            self.on.config_changed: self._on_config_changed,
            self.on.update_status: self._on_update_status,
            self.on.restart_action: self._on_restart_action,
            self.on.start_action: self._on_start_action,
            self.on.stop_action: self._on_stop_action,
        }
        for event, observer in event_observer_mapping.items():
            self.framework.observe(event, observer)

        # Set default values for StoredState
        self._stored.set_default(sip_domain=None)

        self.ingress = IngressRequires(self, self._ingress_config)

    # ---------------------------------------------------------------------------
    #   Properties
    # ---------------------------------------------------------------------------

    @property
    def _ingress_config(self) -> Dict[str, Any]:
        """Ingress configuration property."""
        ingress_config = {
            "service-hostname": self.config.get("external-url", self.app.name),
            "service-name": self.app.name,
            "service-port": 5060,
        }
        if tls_secret_name := self.config.get("tls-secret-name"):
            ingress_config["tls-secret-name"] = tls_secret_name
        return ingress_config

    # ---------------------------------------------------------------------------
    #   Handlers for Charm Events
    # ---------------------------------------------------------------------------

    def _on_config_changed(self, _) -> None:
        """Handler for the config-changed event."""

        # Validate charm configuration
        try:
            self._validate_config()
        except Exception as e:
            self.unit.status = BlockedStatus(f"{e}")
            return

        # Check Pebble has started in the container
        container: Container = self.unit.get_container("kamailio")
        if not container.can_connect():
            logger.debug("waiting for pebble to start")
            self.unit.status = MaintenanceStatus("waiting for pebble to start")
            return

        # Update ingress config
        self.ingress.update_config(self._ingress_config)

        # Add Pebble layer with the Kamailio service
        container.add_layer(
            "kamailio",
            {
                "summary": "kamailio layer",
                "description": "pebble config layer for kamailio",
                "services": {
                    "kamailio": {
                        "override": "replace",
                        "summary": "kamailio",
                        "command": "kamailio -DD -E",
                        "startup": "enabled",
                    }
                },
            },
            combine=True,
        )
        container.replan()

        # Configure kamailio and restart service if needed
        configuration_has_changed = self._configure_kamailio()
        if configuration_has_changed:
            container.restart("kamailio")

        self._on_update_status()

    def _on_update_status(self, _=None) -> None:
        """Handler for the update-status event."""

        # Check if the kamailio service is configured
        container: Container = self.unit.get_container("kamailio")
        if "kamailio" not in container.get_plan().services:
            self.unit.status = WaitingStatus("kamailio service not configured yet")
            return

        # Check if the kamailio service is running
        if container.get_service("kamailio").current == ServiceStatus.ACTIVE:
            self.unit.status = ActiveStatus("kamailio service is running")
        else:
            self.unit.status = BlockedStatus("kamailio service is not running")

    def _on_restart_action(self, event: ActionEvent) -> None:
        """Handler for the restart-action event."""

        try:
            self._restart_kamailio()
            event.set_results({"output": "service restarted"})
        except Exception as e:
            event.fail(f"Failed restarting kamailio: {e}")

    def _on_start_action(self, event: ActionEvent) -> None:
        """Handler for the start-action event."""

        try:
            self._start_kamailio()
            event.set_results({"output": "service started"})
        except Exception as e:
            event.fail(f"Failed starting kamailio: {e}")

    def _on_stop_action(self, event: ActionEvent) -> None:
        """Handler for the stop-action event."""

        try:
            self._stop_kamailio()
            event.set_results({"output": "service stopped"})
        except Exception as e:
            event.fail(f"Failed stopping kamailio: {e}")

    # ---------------------------------------------------------------------------
    #   Validation and configuration
    # ---------------------------------------------------------------------------

    def _validate_config(self) -> None:
        """Validate charm configuration.

        Raises:
            Exception: if charm configuration is invalid.
        """

        # Check if sip-domain config is missing
        if "sip-domain" not in self.config:
            raise Exception('missing charm config: "sip-domain"')

        # Check if sip-domain config value is valid
        if len(self.config.get("sip-domain", "")) < 1:
            raise Exception('"sip-domain" config must be a non-empty string')

    def _configure_kamailio(self) -> bool:
        """Configure kamailio service.

        This function is in charge of pushing configuration files to the container.

        Returns:
            bool: True if the configuration has changed, else False.
        """

        configuration_has_changed = False
        container = self.unit.get_container("kamailio")

        # Configure /etc/kamailio/kamailio-local.cfg
        if not self._file_exists(container, "/etc/kamailio/kamailio-local.cfg"):
            container.push(
                "/etc/kamailio/kamailio-local.cfg",
                "listen=udp:0.0.0.0:5060",
            )
            configuration_has_changed = True

        # Configure /etc/kamailio/kamctlrc
        if self.config["sip-domain"] != self._stored.sip_domain:
            # Backup original configuration file
            if not self._file_exists(container, "/etc/kamailio/kamctlrc.backup"):
                container.push(
                    "/etc/kamailio/kamctlrc.backup",
                    container.pull("/etc/kamailio/kamctlrc").read(),
                )
            container.push(
                "/etc/kamailio/kamctlrc",
                f'SIP_DOMAIN={self.config["sip-domain"]}',
            )
            self._stored.sip_domain = self.config["sip-domain"]
            configuration_has_changed = True
        return configuration_has_changed

    def _file_exists(self, container: Container, path: str) -> bool:
        """Check if a file exists in the container.

        Args:
            path (str): Path of the file to be checked.

        Returns:
            bool: True if the file exists, else False.
        """

        file_exists = None
        try:
            _ = container.pull(path)
            file_exists = True
        except PathError:
            file_exists = False
        except FileNotFoundError:
            file_exists = False
        exist_str = "exists" if file_exists else 'doesn"t exist'
        logger.debug(f"File {path} {exist_str}.")
        return file_exists

    # ---------------------------------------------------------------------------
    #   Kamailio service functions (restart, start, stop)
    # ---------------------------------------------------------------------------

    def _restart_kamailio(self) -> None:
        """Restart kamailio service.

        Raises:
            Exception: if the kamailio service is not configured.
        """

        # Check if kamailio service doesn't exists
        container = self.unit.get_container("kamailio")
        if "kamailio" not in container.get_plan().services:
            raise Exception("kamailio service not configured yet.")

        # Restart kamailio service and update unit status
        container.restart("kamailio")
        self._on_update_status()

    def _start_kamailio(self) -> None:
        """Start kamailio service.

        Raises:
            Exception: if the kamailio service is already running.
        """

        # Check if kamailio service is active
        container = self.unit.get_container("kamailio")
        if container.get_service("kamailio").current == ServiceStatus.ACTIVE:
            raise Exception("kamailio service is already active")

        # Start kamailio service and update unit status
        container.start("kamailio")
        self._on_update_status()

    def _stop_kamailio(self) -> None:
        """Stop kamailio service.

        Raises:
            Exception: if the kamailio service is already stopped.
        """

        # Check if kamailio service isn't active
        container = self.unit.get_container("kamailio")
        if container.get_service("kamailio").current != ServiceStatus.ACTIVE:
            raise Exception("kamailio service is already stopped")

        # Stop kamailio service and update unit status
        container.stop("kamailio")
        self._on_update_status()


if __name__ == "__main__":
    main(KamailioCharm)
