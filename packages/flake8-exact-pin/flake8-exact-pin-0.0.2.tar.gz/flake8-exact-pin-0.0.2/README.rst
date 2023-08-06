flake8-exact-pin
================

Check for exact pins (``==``) of package requirements in ``install_requires``
in ``setup.py``.

For example:

.. code-block:: python

    setup(
        # ...
        install_requires=['pyramid==1.5.6'],
        # ...
    )

Exact pins are often a bad idea, as they:

- Limit flexibility if your package is going to be reused; i.e.: used as a
  library by other Python libraries or applications. You are forcing them to
  use a particular version that they may not want to use or that conflicts with
  what they already use. Not so much of an issue if your package is an
  application rather than a library; however, often `requirements.txt` is a
  better place to manage application requirements that you are pinning (see
  https://caremad.io/blog/setup-vs-requirement/)

- Bake a very strict requirement into your package; you may have to rebuild
  your package just to use a new version of a package with a bug fix.

- Create the potential for hard-to-resolve version conflicts, if you exact pin
  some package versions and don't exact pin others. Some of your other packages
  may require a different version than the one you're pinning and it might be
  impossible for pip to resolve this.

Installation
------------

If you don't already have it, install ``flake8``::

    $ pip install flake8

Then, install the extension::

    $ pip install flake8-exact-pins

Usage
-----

Run the following to verify that the plugin has been installed correctly::

    $ flake8 --version
    2.4.1 (pep8: 1.5.7, flake8-exact-pin: 0.0.0, pyflakes: 0.8.1, mccabe: 0.3) CPython 2.7.9 on Darwin

Now, when you run ``flake8``, the plugin will automatically be used.

When an exact pin is found, ``flake8`` will output something like::

    ./setup.py:28:37: P001 exact pin found in install_requires: "pyramid==1.5.6"
