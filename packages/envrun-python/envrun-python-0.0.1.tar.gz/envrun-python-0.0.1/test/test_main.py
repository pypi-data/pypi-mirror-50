from tempfile import NamedTemporaryFile
import pytest
from envrun.__main__ import main


def test_no_env_no_venv():
    main(["ls -la"])
    assert True


def test_yaml_env_no_venv(env_fixture_yaml):
    for fname in wrap_fixture_file(env_fixture_yaml, suffix=".yaml"):
        main(["-f", fname, "echo $FOO"])
        assert True


def test_dot_env_no_venv(env_fixture_dotenv):
    for fname in wrap_fixture_file(env_fixture_dotenv, suffix=".env"):
        main(["-f", fname, "echo $BAR"])
        assert True


def test_no_env_with_venv():
    """ Note this cheats a bit and assumes .env virtualenv exists """
    main(["-e", ".env", "ls -la"])
    assert True


def test_yaml_env_with_venv(env_fixture_yaml):
    for fname in wrap_fixture_file(env_fixture_yaml, suffix=".yaml"):
        main(["-e", ".env", "-f", fname, "echo $BAZ"])
        assert True


def wrap_fixture_file(fixture, suffix=None):
    with NamedTemporaryFile(suffix=suffix) as f:
        f.write(fixture)
        f.flush()
        yield f.name


@pytest.fixture
def env_fixture_yaml():
    return b"""
FOO: bar
BAR: baz
BAZ: quux
"""


@pytest.fixture
def env_fixture_dotenv():
    return b"""
FOO=bar
BAR =  baz
BAZ =quux
"""
