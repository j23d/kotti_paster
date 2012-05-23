kotti_paster
============

renamed from kotti_addon - documentation has to be updated

kotti_addon is a package which provides "starter" scaffolding for creating an addon for :mod:`Kotti`.

See https://github.com/Pylons/Kotti/blob/master/README.rst for detailed documentation of Kotti.


Installation
------------

Create a virturalenv and get the source code from the git repository:

.. code-block:: text

  $ mkdir kotti-env && cd kotti-env
  $ virtualenv --no-site-packages . && source ./bin/activate
  $ git clone git://github.com/j23d/kotti_addon.git

Use the "setup.py develop" command of your Python interpreter to install the software:

.. code-block:: text

  $ cd kotti_addon
  $ python setup.py develop


Generating an Addon
-------------------

The primary job of :mod:`kotti_addon` is to provide a :term:`scaffold` which
allows you to easily generate an addon for Kotti. You do this with the "pcreate"
command in your virtualenv.

.. code-block:: text

   $ pcreate -t kotti_addon FancyAddon

This will create a ``FancyAddon`` distribution, in which will live a
``fancyaddon`` Python package.


Run it
------

To run the generated addon, use ``pserve`` against the
``development.ini`` file that lives within the distribution directory

.. code-block:: text

   $ pserve FancyAddon/development.ini

The server will be start on port 5000. Visit http://localhost:5000 to see Kotti in
action.

The addon contains example code - change it and add your fancy stuff. See the Kotti
documentation for further informations http://kotti.readthedocs.org/en/latest/index.html.