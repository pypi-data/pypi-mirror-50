tox-wikimedia
=============

Automatically configure tox environments to use standard tools in a
hopefully unobtrusive way.

For example::

    [tox]
    envlist=py{34,35,36,37}-{flake8,pytest}
    skip_missing_interpreters = True
    requires = tox-wikimedia

    [wikimedia]

The following tools are supported for now:

* flake8_
* pytest_

.. _flake8: https://pypi.org/project/flake8/
.. _pytest: https://pytest.org/en/latest/

More to come!
