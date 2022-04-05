from gift_wrap.aws.utils import do_env_variables_exists, get_session_kwargs

from pytest import fixture


@fixture(name="fake_env")
def fixture_fake_env():
    """Sets an fake environment"""

    def dummy_env(env):
        class MockEnvironment:
            environ = env

            def set_env(self, value):
                return self.environ.get(value)

        return MockEnvironment

    yield dummy_env


def test_do_env_variables_exists(fake_env, monkeypatch):
    """Test the correct response is returned if any of the env variables are
    set"""
    env = {"AWS_ACCESS_KEY_ID": "test_access_key_id"}
    monkeypatch.setattr("gift_wrap.aws.utils.os", fake_env(env))
    assert do_env_variables_exists()
    env = {
        "AWS_ACCESS_KEY_ID": "test_access_key_id",
        "AWS_DEFAULT_REGION": "test_region",
        "AWS_SECRET_ACCESS_KEY": "test_secret_access_key",
        "AWS_SESSION_TOKEN": "test_sesion_token",
    }
    monkeypatch.setattr("gift_wrap.aws.utils.os", fake_env(env))
    assert do_env_variables_exists()
    env = {}
    monkeypatch.setattr("gift_wrap.aws.utils.os", fake_env(env))
    assert not do_env_variables_exists()


def test_get_session_kwargs(fake_env, monkeypatch):
    """Test that the aws session kwargs are correctly generated"""
    env = {
        "AWS_ACCESS_KEY_ID": "test_access_key_id",
        "AWS_DEFAULT_REGION": "test_region",
        "AWS_SECRET_ACCESS_KEY": "test_secret_access_key",
        "AWS_SESSION_TOKEN": "test_sesion_token",
    }
    monkeypatch.setattr("gift_wrap.aws.utils.os", fake_env(env))
    assert get_session_kwargs() == {
        "aws_access_key_id": "test_access_key_id",
        "region_name": "test_region",
        "aws_secret_access_key": "test_secret_access_key",
        "aws_session_token": "test_sesion_token",
    }
    env = {"AWS_PROFILE": "profile"}
    monkeypatch.setattr("gift_wrap.aws.utils.os", fake_env(env))
    assert get_session_kwargs() == {"profile_name": "profile"}
