import pytest

from gift_wrap.sample_tracker import SampleTracker
from gift_wrap.sample_tracker.exceptions import SampleTrackerFailedUpload

@pytest.fixture
def sample_tracker_obj():
    """ Creates a Sample Tracker object """
    yield SampleTracker()


def test_sampletracker_post_success(sample_tracker_obj):
    record = {
        "samplename": "fakesample",
        "statekey": "FAKE_STATE",
    }
    response = sample_tracker_obj.post(record)
    assert response == "Upload success"


def test_sampletracker_post_missingkey_samplename(sample_tracker_obj):
    """ Test that an exception is thrown if a samplename is missing """
    record = {
        "samplename": "fakesample",
    }
    with pytest.raises(SampleTrackerFailedUpload) as excinfo:
        sample_tracker_obj.post(record)
        assert "missing statekey" in excinfo.value


def test_sampletracker_post_missingkey_statekey(sample_tracker_obj):
    """ Test that an exception is thrown if a statekey is missing """
    record = {
        "statekey": "fakestate",
    }
    with pytest.raises(SampleTrackerFailedUpload) as excinfo:
        sample_tracker_obj.post(record)
        assert "missing samplename" in excinfo.value
