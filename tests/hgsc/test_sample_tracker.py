"""Test for sample_tracker.py"""
import os
from unittest.mock import patch, MagicMock

import pytest


from gift_wrap.hgsc.sample_tracker import SampleTracker
from gift_wrap.hgsc.exceptions import HGSCWebServiceError


@pytest.fixture(name="sample_tracker")
def fixture_sample_tracker() -> SampleTracker:
    """
    A fixture that provides an object of the
    SampleTracker class.
    """
    token = os.environ["SAMPLE_TRACKER_TOKEN"]
    url = os.environ["SAMPLE_TRACKER_URL"]
    yield SampleTracker(token=token, base_url=url)


def test_sampletracker_post_success(sample_tracker: SampleTracker):
    """Test that sample tracker post successfully"""
    result = sample_tracker.post(
        wgs_sample_internal_id="fake-sample",
        biobank_id="fake-biobank-id",
        project="gift-wrap-test",
        state_key="TEST",
    )
    assert result == "Upload success"


def test_sampletracker_post_fail_httperror(sample_tracker: SampleTracker):
    """Test that if sample tracker fails to post, a SampleFailedUpload exception
    is raised"""
    sample_tracker.base_url = sample_tracker.base_url / "fake"
    with pytest.raises(HGSCWebServiceError):
        sample_tracker.post(
            wgs_sample_internal_id="fake-sample",
            biobank_id="fake-biobank-id",
            project="gift-wrap-test",
            state_key="TEST",
        )


@patch("gift_wrap.hgsc.webservice.http.post")
def test_sampletracker_post_fail_response(
    mock_requests: MagicMock, sample_tracker: SampleTracker
):
    """Test that if sample tracker post but does not return a success, a
    SampleFailedUpload exception is raised."""
    response = {"success": False, "content": "Failed for some reason"}

    class MockResponse:
        """Mock Response"""

        def __init__(self, response, status_code):
            self.json_data = response
            self.status_code = status_code

        def json(self):
            """Json Data"""
            return self.json_data

    mock_requests.return_value = MockResponse(response, 200)
    with pytest.raises(HGSCWebServiceError) as exc_info:
        sample_tracker.post(
            wgs_sample_internal_id="fake-sample",
            biobank_id="fake-biobank-id",
            project="gift-wrap-test",
            state_key="TEST",
        )
    assert "Failed for some reason" in str(exc_info.value.response)
    assert "SampleTracker" in str(exc_info.value.service)


# def test_get_transformed_record():
#     """
#     Test that a given record is correctly transformed to the expected
#     SampleTracker output.
#     """
#     record = get_ungrouped_records("seq_manifest_genome_type")[0]
#     transformed_record = get_transformed_record(record)
#     for field in transformed_record.keys():
#         assert "_" not in field
#     assert "sampleexternalid" in transformed_record
#     assert transformed_record["statekey"] == "bhaou_intake"
#     assert transformed_record["wellposition"] == "A1"
#     assert transformed_record["project"] == "CLAOU"


# @pytest.mark.integration
# def test_post_success(sample_tracker):
#     """
#     Test no exception is raised if the sample is successfully
#     uploaded to the web service.
#     """
#     record = get_ungrouped_records("seq_manifest_genome_type")[0]
#     record.samplename = "TEST"
#     tr = get_transformed_record(record)
#     sample_tracker.post(tr)


# @pytest.mark.integration
# def test_post_failure(sample_tracker):
#     """
#     Test that the SampleFailedUpload exception is raised
#     if the status code of the response is anything but
#     OK (200).
#     """
#     record = get_ungrouped_records("seq_manifest_genome_type")[0]
#     with pytest.raises(SampleFailedUpload):
#         sample_tracker.post(record)
