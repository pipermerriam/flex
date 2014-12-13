import os

import click
from click.testing import CliRunner

from flex.cli import main


DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_flex_cli_schema_validation():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-s',
            os.path.join(DIR, 'schemas/cli-test-valid-schema.yaml'),
        ]
    )

    assert result.exit_code == 0, result.output
    assert result.output == 'Validation passed\n'


def test_flex_cli_schema_validation_with_verbose_argument_name():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '--source',
            os.path.join(DIR, 'schemas/cli-test-valid-schema.yaml'),
        ]
    )

    assert result.exit_code == 0
    assert result.output == 'Validation passed\n'


def test_flex_cli_schema_validation_with_invalid_schema():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '--source',
            os.path.join(DIR, 'schemas/cli-test-invalid-schema.yaml'),
        ]
    )

    assert result.exit_code == 1
    assert "Error: Swagger schema did not validate:" in result.output
    assert "'swagger'" in result.output
    assert "2.1" in result.output
