kotti_paster
============

kotti_paster provides "starter" scaffolding for creating projekt or an addon for :mod:`Kotti`.
See http://kotti.readthedocs.org/en/latest/index.html for detailed documentation of Kotti.

Installation
------------

.. code-block:: text

  $ easy_install kotti_paster

After the installation you have two more paster templates: ``kotti_project`` and ``kotti_addon``.


Create a project
----------------

The ``kotti_project`` :term:`scaffold` allows you to easily generate a buildout based project 
for :mod:`Kotti`. You do this with the "paster create" command in your virtualenv.

.. code-block:: text

   $ paster create -t kotti_project my_project_name

This will create a ``my_project_name`` buildout with a ``my_project_name`` development package.

To run the buildout project bootstrap, run buildout and start your project with ``pserve``:

.. code-block:: text

    $ cd my_project_name
    $ python boostrap.py
    $ ./bin/buildout
    $ ./bin/pserve development.ini

The server will be start on port 6543 on default. Visit http://localhost:6543 to see Kotti with your
addon in  action.

The addon contains example code - change it and add your fancy stuff. See the Kotti
documentation for further informations: http://kotti.readthedocs.org/en/latest/index.html.


Create a addon
--------------

The primary job of :mod:`kotti_paster` is to provide a :term:`scaffold` which
allows you to easily generate an addon for Kotti. You do this with the "pcreate"
command in your virtualenv.

The kotti_addon :term:`scaffold` allows you to create an AddOn for :mod:`Kotti`.

.. code-block:: text

   $ paster create -t kotti_addon my_addon_name

This will create a ``my_addon_name`` package in the current directory. You can use this package
alone inside an own virtualenv for development purposes or you can add it to your buildout.cfg:

.. code-block:: text
[sources]
...
my_addon_name = fs my_addon_name

[application]
...
eggs =
    my_addon_name

and your development.ini:

.. code-block:: text
kotti.configurators =
    ...
    my_addon_name.kotti_configure


The addon contains example code - change it and add your fancy stuff. See the Kotti
documentation for further informations http://kotti.readthedocs.org/en/latest/index.html.


TODO
====

- add content type - or not (default yes)
- add slot example or not (default no)
