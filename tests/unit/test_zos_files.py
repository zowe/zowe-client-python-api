"""Unit tests for the Zowe Python SDK z/OS Files package."""
from unittest import TestCase, mock
from zowe.zos_files_for_zowe_sdk import Files, exceptions


class TestFilesClass(TestCase):
    """File class unit tests."""

    def setUp(self):
        """Setup fixtures for File class."""
        self.test_profile = {"host": "https://mock-url.com",
                                "user": "Username",
                                "password": "Password",
                                "port": 443,
                                "rejectUnauthorized": True
                                }

    def test_object_should_be_instance_of_class(self):
        """Created object should be instance of Files class."""
        files = Files(self.test_profile)
        self.assertIsInstance(files, Files)

    @mock.patch('requests.Session.send')
    def test_delete_uss(self, mock_send_request):
        """Test deleting a directory recursively sends a request"""
        mock_send_request.return_value = mock.Mock(headers={"Content-Type": "application/json"}, status_code=204)

        Files(self.test_profile).delete_uss("filepath_name", recursive=True)
        mock_send_request.assert_called_once()

    @mock.patch('requests.Session.send')
    def test_create_zFS_file_system(self, mock_send_request):
        """Test creating a zfs sends a request"""
        mock_send_request.return_value = mock.Mock(headers={"Content-Type": "application/json"}, status_code=201)

        Files(self.test_profile).create_zFS_file_system("file_system_name", {"perms":100, "cylsPri": 16777213, "cylsSec": 16777215})
        mock_send_request.assert_called_once()

    @mock.patch('requests.Session.send')
    def test_delete_zFS_file_system(self, mock_send_request):
        """Test deleting a zfs sends a request"""
        mock_send_request.return_value = mock.Mock(headers={"Content-Type": "application/json"}, status_code=204)

        Files(self.test_profile).delete_zFS_file_system("file_system_name")
        mock_send_request.assert_called_once()
    
    def test_invalid_permission(self):
        """Test that the correct exception is raised when an invalid permission option is provided"""
        with self.assertRaises(exceptions.InvalidPermsOption) as e_info:
            Files(self.test_profile).create_zFS_file_system("file_system_name", {"perms": -1, "cylsPri": 16777213, "cylsSec": 16777215})
        self.assertEqual(str(e_info.exception), "Invalid zos-files create command 'perms' option: -1")

    def test_invalid_memory_allocation(self):
        """Test that the correct exception is raised when an invalid memory allocation option is provided"""
        with self.assertRaises(exceptions.MaxAllocationQuantityExceeded) as e_info:
            Files(self.test_profile).create_zFS_file_system("file_system_name", {"perms": 775, "cylsPri": 1677755513, "cylsSec": 16777215})
        self.assertEqual(str(e_info.exception), "Maximum allocation quantity of 16777215 exceeded")
    
    @mock.patch('requests.Session.send')
    def test_mount_zFS_file_system(self, mock_send_request):
        """Test mounting a zfs sends a request"""
        mock_send_request.return_value = mock.Mock(headers={"Content-Type": "application/json"}, status_code=204)

        Files(self.test_profile).mount_file_system("file_system_name", "mount_point")
        mock_send_request.assert_called_once()

    @mock.patch('requests.Session.send')
    def test_unmount_zFS_file_system(self, mock_send_request):
        """Test unmounting a zfs sends a request"""
        mock_send_request.return_value = mock.Mock(headers={"Content-Type": "application/json"}, status_code=204)

        Files(self.test_profile).unmount_file_system("file_system_name")
        mock_send_request.assert_called_once()

    @mock.patch('requests.Session.send')
    def test_list_zFS_file_system(self, mock_send_request):
        """Test unmounting a zfs sends a request"""
        mock_send_request.return_value = mock.Mock(headers={"Content-Type": "application/json"}, status_code=200)

        Files(self.test_profile).list_unix_file_systems("file_system_name")
        mock_send_request.assert_called_once()

    def test_create_data_set_raises_error_without_required_arguments(self):
        """Not providing required arguments should raise error."""
        with self.assertRaises(KeyError):
            obj = Files(self.test_profile).create_data_set("DSNAME123", options={
                "alcunit": "CYL",
                "dsorg": "PO",
                "recfm": "FB",
                "blksize": 6160,
                "dirblk": 25
            })

    def test_create_default_data_set_raises_error_for_unsupported_types(self):
        """Attempting to create a data set that is not part of the suggested list should raise error."""
        with self.assertRaises(exceptions.UnsupportedDefaultDataSetRequested) as e_info:
            obj = Files(self.test_profile).create_default_data_set("DSNAME123", "unsuporrted_type")
        
        expected = "Invalid request. The following default options are available: partitioned, sequential, classic, c, binary."
        self.assertEqual(str(e_info.exception), expected)

    @mock.patch('requests.Session.send')
    def test_create_default_dataset_with_partitioned_type(self, mock_send_request):
        """Test creating a partitioned data set sends a request"""
        mock_send_request.return_value = mock.Mock(headers={"Content-Type": "application/json"}, status_code=201)

        Files(self.test_profile).create_default_data_set("dataset_name", "partitioned")
        mock_send_request.assert_called_once()
