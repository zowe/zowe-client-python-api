Basic usage
============

After you install the package in your project, import the class for the required sub-package (i.e `Console` class for z/OS Console commands). 
Create a dictionary to handle communication with the plug-in:

.. code-block:: python

    from zowe.zos_console_for_zowe_sdk import Console
    connection = {
        "host_url": "'<host address>'",
        "user": "<user>",
        "password": "<password>",
    }

    my_console = Console(connection)

Alternatively you can use an existing Zowe CLI profile instead:

.. code-block:: python

    from zowe.zos_console_for_zowe_sdk import Console

    connection = {
        "plugin_profile": "<profile name>>"
    }

    my_console = Console(connection)
