from os import (
    remove,
)
from shutil import rmtree
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
        var('content_type', 'include a Content Type example y/n', default='y'),
    ]

    def post(self, command, output_dir, vars):
        project_dir = join(output_dir, vars['project'])
        test_dir = join(project_dir, 'tests')

        # handle content type
        if not is_true(vars.get('content_type', '')):
            remove(join(project_dir, 'resources.py'))
            remove(join(project_dir, 'views.py'))
            rmtree(join(project_dir, 'templates'), ignore_errors=True)
        else:
            sfd = open(join(test_dir, 'test_content_type.rst'), 'r')
            data = sfd.read()
            sfd.close()
            dfd = open(join(test_dir, 'test_browser.rst'), 'a')
            dfd.write(data)
            dfd.close()
        remove(join(test_dir, 'test_content_type.rst'))


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
