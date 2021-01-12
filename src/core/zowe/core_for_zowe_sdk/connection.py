"""Zowe Python Client SDK.

This program and the accompanying materials are made available under the terms of the
Eclipse Public License v2.0 which accompanies this distribution, and is available at

https://www.eclipse.org/legal/epl-v20.html

SPDX-License-Identifier: EPL-2.0

Copyright Contributors to the Zowe Project.
"""

class ApiConnection:

    def __init__(self, host_url, user, password, ssl_verification):
        """Construct an ApiConnection object."""
        self.host_url = host_url
        self.user = user
        self.password = password
        self.ssl_verification = ssl_verification
