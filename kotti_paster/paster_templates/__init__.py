from os.path import join
from paste.script.templates import (
    Template,
    var,
)
from types import BooleanType


def is_true(value):
    """Determine if the given value is true. This should be changed
    to use the templer.core variables."""
    # Check if we already have a boolean here. This can happen because
    # we call a template in the post of another template, where the
    # variables are already set.
    if type(value) == BooleanType:
        return value
    if value.lower() in ['y', 'yes', 'true']:
        return True
    return False


class KottiTemplateBase(Template):

    use_cheetah = True


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

    vars = [
        var('author', 'Author name'),
        var('author_email', 'Author email'),
        var('content_type', u'Add content type example to the add on? y/n', default='y'),
    ]

    def post(self, command, output_dir, vars):
        for boolflag in ['content_type', ]:
            if is_true(vars.get(boolflag, False)):
                template = templates[boolflag](boolflag)
                template.run(command, output_dir, vars)


class Buildout(KottiProjectBase):
    summary = 'A buildout based Kotti project'

    vars = [
        var('author', 'Author name'),
        var('author_email', 'Author email'),
        var('travis', u'generate a travis configuration file? y/n', default='n'),
        var('gitignore', u'generate a .gitignore file? y/n', default='y')
        # codeintel
        # omelette
        # supervisor
    ]

    def post(self, command, output_dir, vars):
        addon_template = Addon(vars['project'])
        addon_template.run(command, join(output_dir, 'src', vars['project']), vars)
        for boolflag in ['gitignore', 'travis']:
            if is_true(vars.get(boolflag, False)):
                template = templates[boolflag](boolflag)
                template.run(command, output_dir, vars)
