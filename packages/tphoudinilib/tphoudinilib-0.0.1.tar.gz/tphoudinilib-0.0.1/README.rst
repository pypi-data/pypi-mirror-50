tpHoudiniLib
============================================================

.. image:: https://img.shields.io/github/license/tpoveda/tpHoudiniLib.svg
    :target: https://github.com/tpoveda/tpPyUtils/blob/master/LICENSE


Houdini implementation for tpDccLib and tpQtLib packages.

Also, this module contains a lot of utilities functions and classes to work with Houdini Python API (hou)

Installation
-------------------
Manual
~~~~~~~~~~~~~~~~~~~~~~
1. Clone/Download tpHoudiniLib anywhere in your PC (If you download the repo, you will need to extract the contents of the .zip file).
2. Copy **tpHoudiniLib** folder located inside **source** folder in a path added to **sys.path**

Automatic
~~~~~~~~~~~~~~~~~~~~~~
Automatic installation for tpHoudiniLib is not finished yet.

Usage
-------------------
Initialization Code
~~~~~~~~~~~~~~~~~~~~~~
1. If tpDccLib or tpQtLib packages are being used, tpHoudiniLib will be automatic imported during the initialization
of those packages.

2. If tpDccLib and tpQtLib are not found in your sys.path, you will need to initialize manually tpHoudiniLib.

.. code-block:: python

    import tpHoudiniLib
    tpHoudiniLib.init()

Reloading
~~~~~~~~~~~~~~~~~~~~~~
For development purposes, you can enable reloading system, so 
you can reload tpHoudiniLib sources without the necessity of restarting
your Python session. Useful when working with DCCs.

1. If tpDccLib and tpQtLib packages are being used, tpHoudiniLib will be automatic reload by tpDccLib and tpQtLib reload systems.
2. If tpDccLib and tpQtLib are not found, you will need to reload tpHoudiniLib manually.

.. code-block:: python

    import tpHoudiniLib
    reload(tpHoudiniLib)
    tpHoudiniLib.init(True)


Enabling debug log
~~~~~~~~~~~~~~~~~~~~~~
By default, tpHoudiniLib logger only logs warning messages. To enable all log messages
you can set TPHOUDINILIB_DEV environment variables to 'True'

.. code-block:: python

    import os
    
    os.environ['TPHOUDINILIB_DEV'] = 'True'
    import tpHoudiniLib
    tpHoudiniLib.init()
