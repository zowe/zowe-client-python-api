"""Integration tests for the Zowe Python SDK z/OSMF package."""
import unittest
from zowe.zosmf_for_zowe_sdk import Zosmf
from zowe.core_for_zowe_sdk import ProfileManager


class TestZosmfIntegration(unittest.TestCase):
    """Zosmf class integration tests."""

    def setUp(self):
        """Setup fixtures for Zosmf class."""
        test_profile = ProfileManager().load(profile_type="zosmf")
        self.zosmf = Zosmf(test_profile)

    def test_get_info_should_return_valid_response(self):
        """Executing the get_info method should return a valid response."""
        command_output = self.zosmf.get_info()
        self.assertIsInstance(command_output, dict)

    def test_list_systems_should_return_valid_response(self):
        """Executing the list_systems method should return a valid response."""
        command_output = self.zosmf.list_systems()
        self.assertIsInstance(command_output, dict)