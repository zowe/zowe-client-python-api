# Change Log

All notable changes to the Zowe Client Python SDK will be documented in this file.

## Recent Changes

### Enhancements

- Rename Python SDK bundle [#286](https://github.com/zowe/zowe-client-python-sdk/issues/286)
- Added logger class to core SDK [#185](https://github.com/zowe/zowe-client-python-sdk/issues/185)
- Added classes for handling `Datasets`, `USSFiles`, and `FileSystems` in favor of the single Files class. [#264](https://github.com/zowe/zowe-client-python-sdk/issues/264)
- Refactored tests into proper folders and files and add more tests [#265](https://github.com/zowe/zowe-client-python-sdk/issues/265)
- **Breaking:** Standardized `response` outputs based on `Content-Type`. [#266](https://github.com/zowe/zowe-client-python-sdk/issues/266)
- Refactored `create` function in `Datasets` class to accept `DatasetOptions` class as parameters. [#214] (https://github.com/zowe/zowe-client-python-sdk/issues/214)

### Bug Fixes

- Fixed a bug on `_create_custom_request_arguments` where modifications on `custom_arguments` will affect the variable after the function returns. [#299](https://github.com/zowe/zowe-client-python-sdk/issues/299)
- Fixed truncated responses when issuing TSO commands [#260](https://github.com/zowe/zowe-client-python-sdk/issues/260)
- Fixed a bug on `upload_file_to_dsn` where it would not properly convert line endings on Windows. [#104](https://github.com/zowe/zowe-client-python-sdk/issues/104)

## `1.0.0-dev15`

### Bug Fixes

- Fixed error when issuing TSO commands [#255](https://github.com/zowe/zowe-client-python-sdk/issues/255)

## `1.0.0-dev14`

### Enhancements

- Added method `Files.download_uss` to download USS files to disk
- Added support to `Tso` class for loading TSO profile properties

### Bug Fixes

- Fixed `Files.download_dsn` and `Files.download_binary_dsn` failing to write contents to disk [#179](https://github.com/zowe/zowe-client-python-sdk/issues/179)
- Fixed `Files.delete_data_set` and `Files.list_dsn_members` so they encode URLs correctly
- Fixed `Files.upload_to_uss` displaying an unclosed file warning
- Fixed loading environment variables when there is no schema file in current directory

## `1.0.0-dev13`

### Enhancements

- Next Breaking: Updated core SDK method `RequestHandler.perform_streamed_request` to return response object instead of raw buffer. [#245](https://github.com/zowe/zowe-client-python-sdk/pull/245)

### Bug Fixes

- Replaces `datasets` in function names with `data_sets` as a standard and sets unnecessary public variables to private [#83] (https://github.com/zowe/zowe-client-python-sdk/issues/83)
- Fixed `Files.create_data_set` to accept "FBA", "FBM", "VBA", "VBM" as valid recfm [#240](https://github.com/zowe/zowe-client-python-sdk/issues/240)
- Fixed an issue with `Jobs.list_jobs` user correlator parameter [#242](https://github.com/zowe/zowe-client-python-sdk/issues/242)
- Fixed default encoding for I/O operations to be UTF-8 on Windows [#243](https://github.com/zowe/zowe-client-python-sdk/issues/243)

## `1.0.0-dev12`

### Bug Fixes

- Fixed Secrets SDK requiring LD_LIBRARY_PATH to be defined when installed from wheel on Linux [#229](https://github.com/zowe/zowe-client-python-sdk/issues/229)
- Fixed 'issue_command' Console API function to provide custom console name [#231](https://github.com/zowe/zowe-client-python-sdk/issues/231)

## `1.0.0-dev11`

### Enhancements

- Added method to save secure profile properties to vault [#72](https://github.com/zowe/zowe-client-python-sdk/issues/72)
- Added method to save profile properties to zowe.config.json file [#73](https://github.com/zowe/zowe-client-python-sdk/issues/73)
- Added CredentialManager class to securely retrieve values from credentials and manage multiple credential entries on Windows [#134](https://github.com/zowe/zowe-client-python-sdk/issues/134)
- Added method to load profile properties from environment variables [#136](https://github.com/zowe/zowe-client-python-sdk/issues/136)
- Added validation of zowe.config.json file matching the schema [#192](https://github.com/zowe/zowe-client-python-sdk/issues/192)
- Added Secrets SDK for storing client secrets in OS keyring [#208](https://github.com/zowe/zowe-client-python-sdk/issues/208)
- Turned SDK APIs into context manager [#145](https://github.com/zowe/zowe-client-python-sdk/issues/145)

### Bug Fixes

- Fixed profile merge order to match Node.js SDK [#190](https://github.com/zowe/zowe-client-python-sdk/issues/190)
- Fixed issue for datasets and jobs with special characters in URL [#211](https://github.com/zowe/zowe-client-python-sdk/issues/211)
- Fixed exception handling in session.py [#213](https://github.com/zowe/zowe-client-python-sdk/issues/213)
