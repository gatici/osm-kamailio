# Copyright 2022 David Garcia
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest

from charm import SippK8SCharm
from ops.testing import Harness


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(SippK8SCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()
