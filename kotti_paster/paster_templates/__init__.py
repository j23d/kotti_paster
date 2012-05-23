import os
from pyramid.scaffolds import PyramidTemplate
from paste.util.template import paste_script_template_renderer


class KottiAddonTemplate(PyramidTemplate):
    _template_dir = 'kotti_addon'
    summary = 'Kotti AddOn'
    template_renderer = staticmethod(paste_script_template_renderer)

    def pre(self, command, output_dir, vars):
        """Called before template is applied.
        """
        super(KottiAddonTemplate, self).pre(command, output_dir, vars)
        vars['author'] = os.popen2('git config --get user.name')[1].read().strip() or ''
        vars['author_email'] = os.popen2('git config --get user.email')[1].read().strip() or ''
