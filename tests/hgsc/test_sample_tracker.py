"""Test for sample_tracker.py"""
import os
from unittest.mock import patch, MagicMock

import pytest


from gift_wrap.hgsc.sample_tracker import SampleTracker
from gift_wrap.hgsc.exceptions import HGSCWebServiceError
from gift_wrap.hgsc.token import get_token


@pytest.fixture(name="sample_tracker_token")
def fixture_cvl_token():
    """Yield token"""
    client_id = os.environ["SAMPLE_TRACKER_CLIENT_ID"]
    client_secret = os.environ["SAMPLE_TRACKER_CLIENT_SECRET"]
    token_url = os.environ["SAMPLE_TRACKER_TOKEN_URL"]
    yield get_token(
        client_id=client_id, client_secret=client_secret, token_url=token_url
    )


@pytest.fixture(name="sample_tracker")
def fixture_sample_tracker(sample_tracker_token) -> SampleTracker:
    """
    A fixture that provides an object of the
    SampleTracker class.
    """
    url = os.environ["SAMPLE_TRACKER_URL"]
    yield SampleTracker(token=sample_tracker_token, base_url=url)


def test_sampletracker_post_success(sample_tracker: SampleTracker):
    """Test that sample tracker post successfully"""
    result = sample_tracker.post(
        sample_name="fake-sample",
        biobank_id="fake-biobank-id",
        project="gift-wrap-test",
        state_key="TEST",
    )
    assert result
