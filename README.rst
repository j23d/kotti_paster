kotti_paster
============

kotti_paster provides "starter" scaffolding for creating a projekt or an addon for Kotti.
See the `Kotti documentation`_ for detailed documentation.

Installation
------------

You just install the package from PyPi with easy_install. This will install PasteScript and Cheetah.
So you may want to create a new virtualenv to install it there::

  $ easy_install kotti_paster

After the installation you have two more paster templates: ``kotti_project`` and ``kotti_addon``.


Create a project
----------------

The ``kotti_project`` scaffold allows you to easily generate a buildout based project for Kotti. You do this with the "paster create" command in your virtualenv::

   $ paster create -t kotti_project my_project_name

This will create a ``my_project_name`` buildout with a ``my_project_name`` development package.

To run the buildout project bootstrap, run buildout and start your project with ``pserve``::

    $ cd my_project_name
    $ python boostrap.py
    $ ./bin/buildout
    $ ./bin/pserve development.ini

The server will be start on port 6543 on default. Visit http://localhost:6543 to see Kotti with your addon in  action.

The addon contains example code - change it and add your fancy stuff. See the `Kotti documentation`_
for further informations.

There are some parameters to adjust the project to your needs. Some of the options are only available with the ``expert`` mode on the interactive prompt, so choose this if you want to overwrite the defaults of the options ``omelette``, ``codeintel`` and ``supervisor``.

If you use `git`_ as versioning control system a `.gitignore` file is usefull in your project. By default
this file will be created. If you don't need it, set the option `gitignore=false`::

   $ paster create -t kotti_project my_project_name --no-interactive gitignore=false

If you plan to host your project on `github`_ `travis`_ is a handy way to set up continuous integration
with almost no effort. Add the parameter ``travis=true`` to the command line and a file named ``.travis.yml``
will be integrated in your project. This option defaults to ``false``::

   $ paster create -t kotti_project my_project_name  --no-interactive travis=true


`omelette`_ is a recipe that sets up a directory structure that mirrors the actual python namespaces, with 
symlinks to the egg contents. If you won't have this in your buildout, you can exclude it::

   $ paster create -t kotti_project my_project_name --no-interactive omelette=false


The `codeintel`_ recipe generates a configuration file for SublimeCodeIntel, a SublimeText plugin, what is
extremely usefull, but only if you use SublimeText as your editor and have the plugin installed. Use the
command line option ``codeintel`` to activate this option::

   $ paster create -t kotti_project my_project_name --no-interactive codeintel=true


The `supervisor`_ recipe integrates supervisor section to your buildout. Supervisor is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems. Read more about it in the `supervisor documentation`_. Set ``supervisor=true`` on the command line to get this section in your buildout::

   $ paster create -t kotti_project my_project_name --no-interactive supervisor=true



Create a addon
--------------

The primary job of kotti_paster is to provide a scaffold which allows you to easily generate an addon for Kotti. You do this with the ``pcreate`` command in your virtualenv.

The kotti_addon scaffold allows you to create an AddOn for Kotti::

   $ paster create -t kotti_addon my_addon_name

This will create a ``my_addon_name`` package in the current directory. You can use this package alone inside an own virtualenv for development purposes or you can add it to your buildout.cfg::

  [sources]
  ...
  my_addon_name = fs my_addon_name

  [application]
  ...
  eggs =
      my_addon_name

and your development.ini::

  kotti.configurators =
      ...
      my_addon_name.kotti_configure


You can include an example for a Kotti content type, see the `section for content types in the Kotti developer manual`_ for more info::

   $ paster create -t kotti_addon my_addon_name --no-interactive content_type=true

The addon contains example code - change it and add your fancy stuff. See the `Kotti documentation`_ for further informations.


.. _Kotti documentation: http://kotti.readthedocs.org/en/latest/index.html
.. _github: http://github.com
.. _travis: http://travis-ci.org
.. _git: http://git-scm.com/
.. _omelette: http://pypi.python.org/pypi/collective.recipe.omelette
.. _codeintel: http://pypi.python.org/pypi/corneti.recipes.codeintel
.. _supervisor: http://pypi.python.org/pypi/collective.recipe.supervisor
.. _supervisor documentation: http://supervisor.readthedocs.org/en/latest/index.html
.. _section for content types in the Kotti developer manual: http://kotti.readthedocs.org/en/latest/developer-manual.html#content-types
