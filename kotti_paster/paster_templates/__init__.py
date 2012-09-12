import copy
from os.path import join
import subprocess
from templer.core import BasicNamespace
from templer.core.vars import BooleanVar


class KottiTemplateBase(BasicNamespace):
    # for kotti we don't use a dotted namespaces
    dots = 0


class KottiProjectBase(KottiTemplateBase):

    @property
    def _template_dir(self):
        return 'kotti_project/%s' % self.__class__.__name__.lower()


class KottiAddonBase(KottiTemplateBase):

    @property
    def _template_dir(self):
        return 'kotti_addon/%s' % self.__class__.__name__.lower()


class ContentType(KottiAddonBase):
    summary = 'Kotti AddOn base files'


class Git(KottiProjectBase):
    summary = u'generate gitignore file'


class Travis(KottiProjectBase):
    summary = u'generate a travis file'


class Omelette(KottiProjectBase):
    summary = u'add part omelette to buildout'


class Codeintel(KottiProjectBase):
    summary = u'add part codeintel to buildout'


class Supervisor(KottiProjectBase):
    summary = u'add part supervisor to buildout'


templates = dict(
    gitignore=Git,
    travis=Travis,
    omelette=Omelette,
    codeintel=Codeintel,
    supervisor=Supervisor,
    content_type=ContentType,
)


class Addon(KottiAddonBase):
    summary = 'Kotti AddOn base files'

    content_type = BooleanVar('content_type',
        title='Content type example?',
        description='Add content type example to the add-on?',
        default=True)

    name = subprocess.Popen("git config --get user.name",
            stdout=subprocess.PIPE, shell=True).stdout.read().strip()
    email = subprocess.Popen("git config --get user.email",
            stdout=subprocess.PIPE, shell=True).stdout.read().strip()
    defaults = {
        'license_name': 'BSD',
        'keywords': 'kotti addon',
        'url': 'http://pypi.python.org/pypi/',
        'author': name,
        'author_email': email,
    }

    vars = copy.deepcopy(BasicNamespace.vars)
    for var in vars:
        if var.name in defaults:
            var.default = defaults[var.name]
    vars.append(content_type)

    def post(self, command, output_dir, vars):
        for boolflag in ['content_type', ]:
            if getattr(self, boolflag).validate(vars.get(boolflag, 0)):
                template = templates[boolflag](boolflag)
                template.run(command, output_dir, vars)


class Buildout(KottiProjectBase):
    summary = 'A buildout based Kotti project'

    travis = BooleanVar('travis',
        title='Generate a travis configuration file?',
        description='Add a travis configuration file to the buildout?',
        default=False)

    gitignore = BooleanVar('gitignore',
        title='Generate a .gitignore file?',
        description='Add a .gitignore file to the buildout?',
        default=True)

    omelette = BooleanVar('omelette',
        title='Add omelette?',
        description='Add a omelette section to the buildout?',
        default=True)

    codeintel = BooleanVar('codeintel',
        title='Add codeintel?',
        description='Add a codeintel section to the buildout? '\
                    'Only works when also omlette section has been chosen.',
        default=True)

    supervisor = BooleanVar('supervisor',
        title='Add supervisor?',
        description='Add a supervisor section to the buildout?',
        default=True)

    vars = copy.deepcopy(KottiProjectBase.vars)
    vars.extend([travis, gitignore, omelette, codeintel, supervisor])

    def insert_template(self, name):
        """Get the insert file with the part for the option."""
        template = templates[name](name)
        filename = "%s_insert" % name
        return open(join(template.template_dir(), filename)).read()

    def post(self, command, output_dir, vars):
        addon_template = Addon(vars['project'])
        addon_template.run(command, join(output_dir, 'src',
                          vars['project']), vars)
        for boolflag in ['gitignore', 'travis', ]:
            if getattr(self, boolflag).validate(vars.get(boolflag, 0)):
                template = templates[boolflag](boolflag)
                template.run(command, output_dir, vars)
        for boolflag in ['omelette', 'codeintel', 'supervisor', ]:
            if getattr(self, boolflag).validate(vars.get(boolflag, 0)):
                insert_template = self.insert_template(boolflag)
                # get the buildout file and enhance it with the part
                buildout_template = open("%s/buildout.cfg" % output_dir).read()
                buildout_template += "\n%s" % insert_template
                # add the name of the part to the parts section
                insert_point = buildout_template.find('\n\n',
                                buildout_template.find('parts ='))
                buildout_template = buildout_template[:insert_point] +\
                                        "\n" + "    %s" % boolflag +\
                                        buildout_template[insert_point:]
                # write the new template content to the buildout file
                buildout_file = open("%s/buildout.cfg" % output_dir, 'w')
                buildout_file.write(buildout_template)
                buildout_file.close()
