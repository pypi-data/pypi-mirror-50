import unittest
from unittest.mock import patch

from click.testing import CliRunner

import datax.runner as runner

cli_runner = CliRunner()


class TestMain(unittest.TestCase):
    def test_no_args(self):
        result = cli_runner.invoke(runner.main, [])
        self.assertIn('Need query if not using interactive mode', repr(result.exception))
