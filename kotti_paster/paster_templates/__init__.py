from paste.script.templates import (
    Template,
    var,
)


class KottiAddonTemplate(Template):
    _template_dir = 'kotti_addon'
    summary = 'Kotti AddOn'
    use_cheetah = True

    vars = [
        # var('package_name', 'The package name', default='example'),
        var('author', 'Author name'),
        var('author_email', 'Author email'),
    ]
    # __travis (false)
    # __gitsupport (false)
    # __content_type_example (true)
