#!/usr/bin/env python3
# Copyright 2022 David Garcia
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from ops.charm import ActionEvent, CharmBase, PebbleReadyEvent
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, Container

logger = logging.getLogger(__name__)

OPTIONS_XML = """<?xml version="1.0" encoding="us-ascii"?>
<scenario name="Options">
    <send>
        <![CDATA[
OPTIONS sip:[service]@[remote_ip] SIP/2.0
Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]
Max-Forwards: 70
To: <sip:[service]@[remote_ip]>
From: sipp <sip:sipp@[local_ip]:[local_port]>;tag=[call_number]
Call-ID: [call_id]
CSeq: 1 OPTIONS
Contact: <sip:sipp@[local_ip]:[local_port]>
Accept: application/sdp
Content-Length: 0

]]>
    </send>
</scenario>
"""


class SippK8SCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.sipp_pebble_ready, self._on_sipp_pebble_ready)
        self.framework.observe(self.on.options_action, self._on_options_action)

    def _on_sipp_pebble_ready(self, event: PebbleReadyEvent):
        """Handler for the sipp-pebble-ready event."""
        container: Container = event.workload
        container.push("/scenarios/OPTIONS.xml", OPTIONS_XML)
        self.unit.status = ActiveStatus()

    def _on_options_action(self, event: ActionEvent):
        ip = event.params["ip"]
        port = event.params["port"]
        container: Container = self.unit.get_container("sipp")
        try:
            process = container.exec(
                ["sipp", f"{ip}:{port}", "-sf", "OPTIONS.xml", "-m", "5", "-s", "30"],
                working_dir="/scenarios",
            )
            stdout, stderr = process.wait_output()
            event.set_results(
                {
                    "output": "Options action executed successfully",
                    "stdout": stdout,
                    "stderr": stderr,
                }
            )
        except Exception as e:
            event.fail(f"Option action failed: {e}")


if __name__ == "__main__":
    main(SippK8SCharm)
