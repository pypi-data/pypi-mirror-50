tox-local-hooks
================

With this plugin, local tox hook implementations can be defined in a file `toxhooks.py`, which is in the same folder as the tox configuration file.

This will make it easier to write your own custom local hooks for tox. You just have to write the hooks in `toxhooks.py` (instead of creating a plugin package starting with `tox-` and then installing it in the same location as tox).

Example
-------

`tox.ini` file

.. code-block:: bash

    [tox]
    minversion = 3.8.0
    requires = tox-local-hooks
    skipsdist = true

    [testenv]
    whitelist_externals = bash
    randpwdenv = TESTPASSWORD
    commands = bash -c 'echo RANDOM PASSWORD: $TESTPASSWORD'

Then create the `toxhooks.py` file in the same folder as `tox-ini` file

.. code-block:: python

    import pluggy, string, random

    hookimpl = pluggy.HookimplMarker("tox")

    @hookimpl
    def tox_addoption(parser):
        parser.add_testenv_attribute(
            "randpwdenv",
            type="string",
            help="Random password environmental variable"
        )

    @hookimpl(tryfirst=True)
    def tox_configure(config):
        for envConf in config.envconfigs.values():
            if envConf.randpwdenv:
                pwd = ''.join(random.choice(string.ascii_letters) for _ in range(10))
                envConf.setenv[envConf.randpwdenv] = pwd


While running `tox`, you should be able to see the following output

.. code-block::

    RANDOM PASSWORD: {some_random_string}
