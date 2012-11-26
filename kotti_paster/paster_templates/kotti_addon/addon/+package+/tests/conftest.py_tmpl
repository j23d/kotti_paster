pytest_plugins = "kotti"

from pytest import fixture


def tnc_settings():
    from kotti import _resolve_dotted
    from kotti import conf_defaults
    settings = conf_defaults.copy()
    settings['kotti.secret'] = 'secret'
    settings['kotti.secret2'] = 'secret2'
    settings['pyramid.includes'] += ''' tnc_theme.views.timeline
        tnc_theme.views.persons
        tnc_theme.views.quotes
        tnc_theme.views.views
        pyramid_snippets
        tnc_theme.snippets
        tnc_theme.widgets
        kotti_blog.views'''
    settings['kotti.available_types'] += ''' tnc_theme.resources.Persons
        tnc_theme.resources.Persons
        tnc_theme.resources.Person
        tnc_theme.resources.Institutions
        tnc_theme.resources.Institution
        tnc_theme.resources.Quote
        tnc_theme.resources.SecureDocument
        tnc_theme.resources.TimelineFolder
        tnc_theme.resources.TimelineMilestone
        tnc_theme.resources.TimelineContent
        kotti_blog.resources.Blog
        kotti_blog.resources.BlogEntry'''
    settings['kotti.asset_overrides'] += ' tnc_theme:kotti-overrides/'
    settings['kotti.populators'] = 'tnc_theme.populate.populate'
    settings['kotti.templates.api'] = 'tnc_theme.utils.TncTemplateAPI'
    settings['kotti.alembic_dirs'] += ' tnc_theme:alembic'
    # settings['kotti.root_factory'] = 'tnc_theme.utils.get_root'
    settings['kotti.use_workflow'] = 'tnc_theme:workflow.zcml'
    _resolve_dotted(settings)
    return settings


@fixture
def tnc_populate(db_session):
    from transaction import commit
    # remove content created by kotti default populator
    from kotti import DBSession
    from kotti.resources import get_root
    DBSession.delete(get_root())
    for populate in tnc_settings()['kotti.populators']:
        populate()
    commit()


@fixture(scope='function')
def tnc_config(request):
    from pyramid.config import DEFAULT_RENDERERS
    from pyramid import testing
    from kotti import security
    config = testing.setUp(settings=tnc_settings())
    for name, renderer in DEFAULT_RENDERERS:
        config.add_renderer(name, renderer)
    request.addfinalizer(security.reset)
    request.addfinalizer(testing.tearDown)
    return config


@fixture(scope='session')
def tnc_connection():
    # the following setup is based on `kotti.resources.initialize_sql`,
    # except that it explicitly binds the session to a specific connection
    # enabling us to use savepoints independent from the orm, thus allowing
    # to `rollback` after using `transaction.commit`...
    from transaction import commit
    from sqlalchemy import create_engine
    from kotti.testing import testing_db_url
    from kotti import metadata, DBSession
    engine = create_engine(testing_db_url())
    connection = engine.connect()
    DBSession.registry.clear()
    DBSession.configure(bind=connection)
    metadata.bind = engine
    metadata.drop_all(engine)
    metadata.create_all(engine)
    for populate in tnc_settings()['kotti.populators']:
        populate()
    commit()
    return connection


@fixture
def tnc_db_session(tnc_config, tnc_connection, request):
    from transaction import abort
    trans = tnc_connection.begin()          # begin a non-orm transaction
    request.addfinalizer(trans.rollback)
    request.addfinalizer(abort)
    from kotti import DBSession
    return DBSession()
