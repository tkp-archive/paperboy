from mock import patch, MagicMock


class TestConfig:
    def test_import1(self):
        from paperboy.server import main
