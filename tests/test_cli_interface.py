from src.cli.cli_interface import CLIInterface


class TestCLIInterface:
    def setup_method(self):
        self.cli = CLIInterface()

    def test_cli_initialization(self):
        cli = CLIInterface()
        assert cli.merger is not None
        assert cli.detector is not None
