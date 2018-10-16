# -*- coding: utf8 -*-


import pytest

from usmqe.api.tendrlapi.common import TendrlApi, login, logout
from plugin.usm_config import UsmConfig

config = UsmConfig()


@pytest.mark.happypath
@pytest.mark.testready
def test_login_valid(valid_session_credentials):
    api = TendrlApi(auth=valid_session_credentials)
    api.jobs()


@pytest.mark.testready
def test_login_invalid():
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    auth = login("invalid_user", "invalid_password", asserts_in=asserts)
    api = TendrlApi(auth)
    api.jobs(asserts_in=asserts)


@pytest.mark.testready
def test_session_unauthorized():
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    # passing auth=None would result in api requests to be done without Tendrl
    # auth header
    api = TendrlApi(auth=None)
    api.jobs(asserts_in=asserts)


@pytest.mark.testready
def test_session_invalid(invalid_session_credentials):
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    api = TendrlApi(auth=invalid_session_credentials)
    api.jobs(asserts_in=asserts)


@pytest.mark.happypath
@pytest.mark.testready
def test_login_multiple_sessions():
    auth_one = login(
        config.config["tests"]["usm_username"],
        config.config["tests"]["usm_password"])
    auth_two = login(
        config.config["tests"]["usm_username"],
        config.config["tests"]["usm_password"])
    logout(auth=auth_one)
    logout(auth=auth_two)


@pytest.mark.testready
def test_login_multiple_sessions_twisted():
    asserts = {
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401,
        }
    api_one = TendrlApi(auth=login(
        config.config["tests"]["usm_username"],
        config.config["tests"]["usm_password"]))
    api_two = TendrlApi(auth=login(
        config.config["tests"]["usm_username"],
        config.config["tests"]["usm_password"]))
    api_one.jobs()
    api_two.jobs()
    logout(auth=api_one._auth)
    api_one.jobs(asserts_in=asserts)
    api_two.jobs()
    logout(auth=api_two._auth)
    api_one.jobs(asserts_in=asserts)
    api_two.jobs(asserts_in=asserts)
