from os import remove
from os.path import join
from paste.script.templates import (
    Template,
    var,
)


class KottiAddonTemplate(Template):
    _template_dir = 'kotti_addon'
    summary = 'Kotti AddOn'
    use_cheetah = True

    vars = [
        var('author', 'Author name'),
        var('author_email', 'Author email'),
        # __content_type_example (true)
    ]


def is_true(value):
    if value.lower() in ['y', 'yes', 'true']:
        return True
    return False


class KottiProjectTemplate(Template):
    _template_dir = 'kotti_project'
    summary = 'A buildout based Kotti project'
    use_cheetah = True

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
        if not is_true(vars['travis']):
            remove(join(output_dir, '.travis.yml'))
        if not is_true(vars['gitignore']):
            remove(join(output_dir, '.gitignore'))
