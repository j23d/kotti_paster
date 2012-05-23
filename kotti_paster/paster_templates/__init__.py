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


class KottiProjectTemplate(Template):
    _template_dir = 'kotti_project'
    summary = 'A buildout based Kotti project'
    use_cheetah = True

    vars = [
        var('author', 'Author name'),
        var('author_email', 'Author email'),
        var('travis', u'generate travis configuration file', default=False)
    ]
    # __gitsupport (false)

    def post(self, command, output_dir, vars):
        addon_template = KottiAddonTemplate(vars['project'])
        addon_template.run(command, join(output_dir, 'src', vars['project']), vars)
