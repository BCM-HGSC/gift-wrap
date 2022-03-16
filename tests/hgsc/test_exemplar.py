import os
import pytest

from gift_wrap.hgsc.exemplar import ExemplarAPI


@pytest.fixture(name="exemplar_api")
def fixture_exemplar_api():
    """Yields an authenticated ExemplarLims client"""
    token = os.environ["EXEMPLAR_TOKEN"]
    url = os.environ["EXEMPLAR_URL"]
    verify_ssl = os.environ["EXEMPLAR_SSL"]
    yield ExemplarAPI(token, url, verify_ssl)


def test_get_drc_ready_samples(exemplar_api: ExemplarAPI):
    """Test that `get_samples` returns the expected list of samples when
    calling the expected DRC url."""
    results = exemplar_api.get_drc_ready_samples()
    assert results


# # TODO: Need to figure out how to do this better.
# def test_push_sample_success_drc_success(exemplar_api: ExemplarAPI):
#     """
#     Positive use case smoke test when pushing a DRC success.
#     """
#     date_submitted = "2021-01-27 10:10:10"
#     lane_barcode_or_merge_name = "HIJFVYPG-1-IDUDI0083"
#     expected_result = {
#         "dataRecord": None,
#         "success": False,
#         "message": "Success: Submission status was set successfully.",
#     }
#     result = exemplar_api.push_sample_success(
#         lane_barcode_or_merge_name, date_submitted
#     )
#     assert result == expected_result


# @pytest.mark.integration
# def test_push_sample_success_failure(exemplar_api):
#     """
#     Test that the exception UnableToPushSampleSuccess is raised if the application
#     was able to post but was not successful in LIMS (datetime is wrong or lanebarcode
#     does not exist)
#     """
#     date_submitted = "2021-01-27 10:10:10"
#     lane_barcode_or_merge_name = "test_barcode"
#     with pytest.raises(module.UnableToPushSampleSuccess):
#         exemplar_api.push_sample_success(lane_barcode_or_merge_name, date_submitted)
