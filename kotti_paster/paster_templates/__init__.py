import copy
from os.path import join
from templer.core.vars import BooleanVar
from templer.core import BasicNamespace


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


templates = dict(
    gitignore=Git,
    travis=Travis,
    content_type=ContentType,
)


class Addon(KottiAddonBase):
    summary = 'Kotti AddOn base files'

    content_type = BooleanVar('content_type',
        title='Content type example?',
        description='Add content type example to the add-on?',
        default=True)

    vars = copy.deepcopy(BasicNamespace.vars)
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

    vars = copy.deepcopy(KottiProjectBase.vars)
    vars.extend([travis, gitignore, ])

    # codeintel
    # omelette
    # supervisor

    def post(self, command, output_dir, vars):
        addon_template = Addon(vars['project'])
        addon_template.run(command, join(output_dir, 'src', vars['project']), vars)
        for boolflag in ['gitignore', 'travis']:
            if getattr(self, boolflag).validate(vars.get(boolflag, 0)):
                template = templates[boolflag](boolflag)
                template.run(command, output_dir, vars)
