from os.path import join
from paste.script.templates import (
    Template,
    var,
)


def is_true(value):
    if value.lower() in ['y', 'yes', 'true']:
        return True
    return False


class KottiAddonTemplate(Template):
    _template_dir = 'kotti_addon'
    summary = 'Kotti AddOn'
    use_cheetah = True

    vars = [
        var('author', 'Author name'),
        var('author_email', 'Author email'),
        # __content_type_example (true)
    ]


class KottiTemplateBase(Template):

    use_cheetah = True

    @property
    def _template_dir(self):
        return 'kotti_project/%s' % self.__class__.__name__.lower()


class Git(KottiTemplateBase):
    summary = u'generate gitignore file'


class Travis(KottiTemplateBase):
    summary = u'generate a travis file'


templates = dict(
    gitignore=Git,
    travis=Travis,
)


class Buildout(KottiTemplateBase):
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
        addon_template = KottiAddonTemplate(vars['project'])
        addon_template.run(command, join(output_dir, 'src', vars['project']), vars)
        for boolflag in ['gitignore', 'travis']:
            if is_true(vars.get(boolflag, False)):
                template = templates[boolflag](boolflag)
                template.run(command, output_dir, vars)
