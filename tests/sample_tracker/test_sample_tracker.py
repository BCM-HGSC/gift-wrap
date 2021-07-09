import pytest

from gift_wrap.sample_tracker import SampleTracker
import logging

@pytest.fixture
def sample_tracker_obj():
    """ Creates a Sample Tracker object """
    yield SampleTracker()


def test_sampletracker_post_success(sample_tracker_obj, caplog):
    caplog.set_level(logging.DEBUG)
    record = {
        "samplename": "fakesample",
        "statekey": "FAKE_STATE",
    }
    response = sample_tracker_obj.post(record)
    assert response == "Upload success"


