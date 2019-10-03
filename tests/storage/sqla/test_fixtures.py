
class TestFixtures:
    def test_run_fixtures(self):
        from paperboy.storage.sqla.fixtures import main
        main('sqlite:///:memory:')
