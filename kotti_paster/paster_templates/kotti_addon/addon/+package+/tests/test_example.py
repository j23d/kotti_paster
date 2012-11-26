# This class expects to be useless, except from the point
# of storytelling. It tells you the story that you can use
# all the nice pytest fixtures from Kotti itself in your
# tests without the need of deriving from UnitTestCase.

# The db_session parameter is a fixture, defined in here:
# https://github.com/Pylons/Kotti/blob/master/kotti/tests/configure.py
# If you don't know about pytest fixtures, take a deeper
# look here: http://pytest.org/latest/fixture.html.


class TestExample:

    def test_root(self, db_session):
        from kotti.resources import get_root
        root = get_root()
        assert root is not None
