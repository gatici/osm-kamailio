# Copyright 2021 Gabor Meszaros
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest
from unittest.mock import Mock

from charm import KamailioCharm
from ops.testing import Harness
from ops.model import ActiveStatus, BlockedStatus, MaintenanceStatus


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(KamailioCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()
        container = self.harness.charm.unit.get_container("kamailio")
        container.push("/etc/kamailio/kamctlrc", "", make_dirs=True)

    def test_invalid_config(self):
        self.harness.update_config({"sip-domain": ""})
        self.assertEqual(
            self.harness.charm.unit.status,
            BlockedStatus('"sip-domain" config must be a non-empty string'),
        )

    def test_pebble_not_ready(self):
        get_container_mock = Mock()
        container_mock = Mock()
        container_mock.can_connect.return_value = False
        get_container_mock.return_value = container_mock
        self.harness.charm.unit.get_container = get_container_mock
        self.harness.update_config({"sip-domain": "another.domain"})
        self.assertEqual(
            self.harness.charm.unit.status,
            MaintenanceStatus("waiting for pebble to start"),
        )

    def test_valid_config(self):
        self.assertEqual(self.harness.charm._stored.sip_domain, None)
        self.harness.charm.on.kamailio_pebble_ready.emit("kamailio")
        self.assertEqual(self.harness.charm._stored.sip_domain, "localhost")
        self.harness.update_config(
            {
                "sip-domain": "another.domain",
                "tls-secret-name": "my-tls-secret-name",
            }
        )
        self.assertEqual((self.harness.charm._stored.sip_domain), "another.domain")
        self._assert_container_running()

    def test_restart_action(self):
        action_event = Mock()
        self.harness.charm.on.kamailio_pebble_ready.emit("kamailio")
        self.harness.charm._on_restart_action(action_event)
        action_event.set_results.assert_called_with({"output": "service restarted"})
        self._assert_container_running()

    def test_start_action(self):
        action_event = Mock()
        self.harness.charm.on.kamailio_pebble_ready.emit("kamailio")
        self.harness.charm._on_start_action(action_event)
        self.assertTrue(action_event.fail.called)
        self.assertFalse(action_event.set_results.called)
        # The service start automaticaly,
        # so we need to stop the service for the start action to work.
        self.harness.charm._on_stop_action(action_event)
        self.harness.charm._on_start_action(action_event)
        action_event.set_results.assert_called_with({"output": "service started"})
        self._assert_container_running()

    def test_stop_action(self):
        action_event = Mock()
        self.harness.charm.on.kamailio_pebble_ready.emit("kamailio")
        self.harness.charm._on_stop_action(action_event)
        action_event.set_results.assert_called_with({"output": "service stopped"})
        self.assertEqual(
            self.harness.charm.unit.status,
            BlockedStatus("kamailio service is not running"),
        )

    def _assert_container_running(self):
        self.assertEqual(
            self.harness.charm.unit.status,
            ActiveStatus("kamailio service is running"),
        )
