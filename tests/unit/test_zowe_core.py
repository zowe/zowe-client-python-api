"""Unit tests for the Zowe Python SDK Core package."""

# Including necessary paths
import base64
import json
import os
import shutil
import sys
import unittest
from unittest import mock
from unittest.mock import patch
from jsonschema import validate, ValidationError
from zowe.core_for_zowe_sdk.validators import validate_config_json
import commentjson

from pyfakefs.fake_filesystem_unittest import TestCase
from zowe.core_for_zowe_sdk import (
    ApiConnection,
    ConfigFile,
    ProfileManager,
    RequestHandler,
    SdkApi,
    ZosmfProfile,
    exceptions,
    session_constants,
    custom_warnings,
)

FIXTURES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
CWD = os.getcwd()
CRED_DICT: dict = {}
SECURE_CONFIG_PROPS: bytes


def keyring_get_password(serviceName: str, username: str):
    global SECURE_CONFIG_PROPS
    return SECURE_CONFIG_PROPS


def keyring_get_password_exception():
    raise Exception


class TestApiConnectionClass(unittest.TestCase):
    """ApiConnection class unit tests."""

    def setUp(self):
        """Setup ApiConnection fixtures."""
        self.url = "https://mock-url.com"
        self.user = "Username"
        self.password = "Password"

    def test_object_should_be_instance_of_class(self):
        """Created object should be instance of ApiConnection class."""
        api_connection = ApiConnection(self.url, self.user, self.password)
        self.assertIsInstance(api_connection, ApiConnection)

    def test_object_should_raise_custom_error_without_url(self):
        """Instantiation of ApiConnection object should raise MissingConnectionArgs if host_url is blank."""
        with self.assertRaises(exceptions.MissingConnectionArgs):
            ApiConnection(host_url="", user=self.user, password=self.password)

    def test_object_should_raise_custom_error_without_user(self):
        """Instantiation of ApiConnection object should raise MissingConnectionArgs if user is blank."""
        with self.assertRaises(exceptions.MissingConnectionArgs):
            ApiConnection(host_url=self.url, user="", password=self.password)

    def test_object_should_raise_custom_error_without_password(self):
        """Instantiation of ApiConnection object should raise MissingConnectionArgs if password is blank."""
        with self.assertRaises(exceptions.MissingConnectionArgs):
            ApiConnection(host_url=self.url, user=self.user, password="")


class TestSdkApiClass(TestCase):
    """SdkApi class unit tests."""

    def setUp(self):
        """Setup fixtures for SdkApi class."""
        common_props = {
            "host": "mock-url.com",
            "port": 443,
            "protocol": "https",
            "rejectUnauthorized": True
        }
        self.basic_props = {**common_props, "user": "Username", "password": "Password"}
        self.bearer_props = {**common_props, "tokenValue": "BearerToken"}
        self.token_props = {
            **common_props,
            "tokenType": "MyToken",
            "tokenValue": "TokenValue",
        }
        self.default_url = "https://default-api.com/"

    def test_object_should_be_instance_of_class(self):
        """Created object should be instance of SdkApi class."""
        sdk_api = SdkApi(self.basic_props, self.default_url)
        self.assertIsInstance(sdk_api, SdkApi)

    def test_should_handle_basic_auth(self):
        """Created object should handle basic authentication."""
        sdk_api = SdkApi(self.basic_props, self.default_url)
        self.assertEqual(sdk_api.session.type, session_constants.AUTH_TYPE_BASIC)
        self.assertEqual(
            sdk_api.request_arguments["auth"],
            (self.basic_props["user"], self.basic_props["password"]),
        )

    def test_should_handle_bearer_auth(self):
        """Created object should handle bearer authentication."""
        sdk_api = SdkApi(self.bearer_props, self.default_url)
        self.assertEqual(sdk_api.session.type, session_constants.AUTH_TYPE_BEARER)
        self.assertEqual(
            sdk_api.default_headers["Authorization"],
            "Bearer " + self.bearer_props["tokenValue"],
        )

    def test_should_handle_token_auth(self):
        """Created object should handle token authentication."""
        sdk_api = SdkApi(self.token_props, self.default_url)
        self.assertEqual(sdk_api.session.type, session_constants.AUTH_TYPE_TOKEN)
        self.assertEqual(
            sdk_api.default_headers["Cookie"],
            self.token_props["tokenType"] + "=" + self.token_props["tokenValue"],
        )


class TestRequestHandlerClass(unittest.TestCase):
    """RequestHandler class unit tests."""

    def setUp(self):
        """Setup fixtures for RequestHandler class."""
        self.session_arguments = {"verify": False}

    def test_object_should_be_instance_of_class(self):
        """Created object should be instance of RequestHandler class."""
        request_handler = RequestHandler(self.session_arguments)
        self.assertIsInstance(request_handler, RequestHandler)

    @mock.patch("requests.Session.send")
    def test_perform_streamed_request(self, mock_send_request):
        """Performing a streamed request should call 'send_request' method"""
        mock_send_request.return_value = mock.Mock(status_code=200)
        request_handler = RequestHandler(self.session_arguments)
        request_handler.perform_streamed_request("GET", {"url": "https://www.zowe.org"})
        mock_send_request.assert_called_once()
        self.assertTrue(mock_send_request.call_args[1]["stream"])


class TestZosmfProfileClass(unittest.TestCase):
    """ZosmfProfile class unit tests."""

    def setUp(self):
        """Setup fixtures for ZosmfProfile class."""
        self.profile_name = "MOCK"

    def test_object_should_be_instance_of_class(self):
        """Created object should be instance of ZosmfProfile class."""
        zosmf_profile = ZosmfProfile(self.profile_name)
        self.assertIsInstance(zosmf_profile, ZosmfProfile)


class TestZosmfProfileManager(TestCase):
    """ProfileManager class unit tests."""

    def setUp(self):
        """Setup fixtures for ZosmfProfile class."""
        # setup pyfakefs
        self.setUpPyfakefs()
        self.original_file_path = os.path.join(FIXTURES_PATH, "zowe.config.json")
        self.original_user_file_path = os.path.join(
            FIXTURES_PATH, "zowe.config.user.json"
        )
        self.fs.add_real_file(self.original_file_path)
        self.fs.add_real_file(self.original_user_file_path)

        self.custom_dir = os.path.dirname(FIXTURES_PATH)
        self.custom_appname = "zowe_abcd"
        self.custom_filename = f"{self.custom_appname}.config.json"

        # setup keyring
        home = os.path.expanduser("~")
        self.global_config_path = os.path.join(home, ".zowe", "zowe.config.json")

    def setUpCreds(self, file_path, secure_props):
        global CRED_DICT
        # we are not storing global config properties since they are not
        # accessible within pyfakefs
        # todo : add a test that check loading from gloabl config path
        CRED_DICT = {
            file_path: secure_props,
        }

        global SECURE_CONFIG_PROPS
        SECURE_CONFIG_PROPS = base64.b64encode((json.dumps(CRED_DICT)).encode("utf-8"))
        if sys.platform == "win32":
            SECURE_CONFIG_PROPS = SECURE_CONFIG_PROPS.decode("utf-16")

    @patch("keyring.get_password", side_effect=keyring_get_password)
    def test_autodiscovery_and_base_profile_loading(self, get_pass_func):
        """
        Test loading of correct file by autodiscovering from current working directory
        also load by profile_type correctly populating fields from base profile
        and secure credentials
        """

        # Setup - copy profile to fake filesystem created by pyfakefs
        cwd_up_dir_path = os.path.dirname(CWD)
        cwd_up_file_path = os.path.join(cwd_up_dir_path, "zowe.config.json")
        os.chdir(CWD)
        shutil.copy(self.original_file_path, cwd_up_file_path)

        self.setUpCreds(cwd_up_file_path, {
            "profiles.base.properties.user": "user",
            "profiles.base.properties.password": "password",
        })

        # Test
        prof_manager = ProfileManager()
        props: dict = prof_manager.load(profile_type="base")
        self.assertEqual(prof_manager.config_filepath, cwd_up_file_path)

        expected_props = {
            "host": "zowe.test.cloud",
            "rejectUnauthorized": False,
            "user": "user",
            "password": "password",
        }
        self.assertEqual(props, expected_props)

    @patch("keyring.get_password", side_effect=keyring_get_password)
    def test_custom_file_and_custom_profile_loading(self, get_pass_func):
        """
        Test loading of correct file given a filename and directory,
        also load by profile_name correctly populating fields from custom
        profile and secure credentials
        """
        # Setup - copy profile to fake filesystem created by pyfakefs
        custom_file_path = os.path.join(self.custom_dir, self.custom_filename)
        shutil.copy(self.original_file_path, custom_file_path)

        self.setUpCreds(custom_file_path, {
            "profiles.zosmf.properties.user": "user",
            "profiles.zosmf.properties.password": "password",
        })

        # Test
        prof_manager = ProfileManager(appname=self.custom_appname)
        prof_manager.config_dir = self.custom_dir
        props: dict = prof_manager.load(profile_name="zosmf")
        self.assertEqual(prof_manager.config_filepath, custom_file_path)

        expected_props = {
            "host": "zowe.test.cloud",
            "rejectUnauthorized": False,
            "user": "user",
            "password": "password",
            "port": 10443,
        }
        self.assertEqual(props, expected_props)

    @patch("keyring.get_password", side_effect=keyring_get_password)
    def test_profile_loading_with_user_overriden_properties(self, get_pass_func):
        """
        Test overriding of properties from user config,
        also load by profile_name correctly populating fields from base profile
        and secure credentials
        """

        cwd_up_dir_path = os.path.dirname(CWD)
        cwd_up_file_path = os.path.join(cwd_up_dir_path, "zowe.config.json")
        os.chdir(CWD)
        shutil.copy(self.original_file_path, cwd_up_file_path)
        shutil.copy(self.original_user_file_path, cwd_up_dir_path)

        self.setUpCreds(cwd_up_file_path, {
            "profiles.zosmf.properties.user": "user",
            "profiles.zosmf.properties.password": "password",
        })

        # Test
        prof_manager = ProfileManager()
        props: dict = prof_manager.load(profile_type="zosmf")
        self.assertEqual(prof_manager.config_filepath, cwd_up_file_path)

        expected_props = {
            "host": "zowe.test.user.cloud",
            "rejectUnauthorized": False,
            "user": "user",
            "password": "password",
            "port": 10000,
        }
        self.assertEqual(props, expected_props)

    @patch("keyring.get_password", side_effect=keyring_get_password)
    def test_profile_loading_exception(self, get_pass_func):
        """
        Test correct exceptions are being thrown when a profile is
        not found.

        Only the filename will be set
        """
        with self.assertRaises(exceptions.ProfileNotFound):
            # Setup
            cwd_up_dir_path = os.path.dirname(CWD)
            cwd_up_file_path = os.path.join(
                cwd_up_dir_path, f"{self.custom_appname}.config.json"
            )
            os.chdir(CWD)
            shutil.copy(self.original_file_path, cwd_up_file_path)

            # Test
            config_file = ConfigFile(name=self.custom_appname, type="team_config")
            props: dict = config_file.get_profile(profile_name="non_existent_profile")

    @patch("keyring.get_password", side_effect=keyring_get_password_exception)
    def test_secure_props_loading_warning(self, get_pass_func):
        """
        Test correct warnings are being thrown when secure properties
        are not found in keyring.

        Only the config folder will be set
        """
        with self.assertWarns(custom_warnings.SecurePropsNotFoundWarning):
            # Setup
            custom_file_path = os.path.join(self.custom_dir, "zowe.config.json")
            shutil.copy(self.original_file_path, custom_file_path)

            # Test
            prof_manager = ProfileManager()
            prof_manager.config_dir = self.custom_dir
            props: dict = prof_manager.load("base")

    @patch("keyring.get_password", side_effect=keyring_get_password)
    def test_profile_not_found_warning(self, get_pass_func):
        """
        Test correct warnings are being thrown when profile is not found
        in config file.

        Only the config folder will be set
        """
        with self.assertWarns(custom_warnings.ProfileNotFoundWarning):
            # Setup
            custom_file_path = os.path.join(self.custom_dir, "zowe.config.json")
            shutil.copy(self.original_file_path, custom_file_path)

            # Test
            prof_manager = ProfileManager()
            prof_manager.config_dir = self.custom_dir
            props: dict = prof_manager.load("non_existent_profile")


class TestValidateConfigJsonClass(unittest.TestCase):
    """Testing the validate_config_json function"""

    def test_validate_config_json_valid(self):
        """Test validate_config_json with valid config.json matching schema.json"""
        path_to_config = FIXTURES_PATH + "/zowe.config.json"
        path_to_schema = FIXTURES_PATH + "/zowe.schema.json"

        config_json = commentjson.load(open(path_to_config))
        schema_json = commentjson.load(open(path_to_schema))

        expected = validate(config_json, schema_json)
        result = validate_config_json(path_to_config, path_to_schema)

        self.assertEqual(result, expected)

    def test_validate_config_json_invalid(self):
        """Test validate_config_json with invalid config.json that does not match schema.json"""
        path_to_invalid_config = FIXTURES_PATH + "/invalid.zowe.config.json"
        path_to_invalid_schema = FIXTURES_PATH + "/invalid.zowe.schema.json"

        invalid_config_json = commentjson.load(open(path_to_invalid_config))
        invalid_schema_json = commentjson.load(open(path_to_invalid_schema))

        with self.assertRaises(ValidationError) as expected_info:
            validate(invalid_config_json, invalid_schema_json)

        with self.assertRaises(ValidationError) as actual_info:
            validate_config_json(path_to_invalid_config, path_to_invalid_schema)

        self.assertEqual(str(actual_info.exception), str(expected_info.exception))
