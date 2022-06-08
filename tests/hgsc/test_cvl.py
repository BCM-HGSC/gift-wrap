import os

import pytest

from gift_wrap.hgsc.cvl import CVLAPI
from gift_wrap.hgsc.exceptions import HGSCWebServiceError
from gift_wrap.utils.token import get_token


@pytest.fixture(name="cvl_token")
def fixture_cvl_token():
    """Yield token"""
    client_id = os.environ["CVL_API_CLIENT_ID"]
    client_secret = os.environ["CVL_API_CLIENT_SECRET"]
    token_url = os.environ["CVL_API_TOKEN_URL"]
    yield get_token(
        client_id=client_id, client_secret=client_secret, token_url=token_url
    )


@pytest.fixture(name="cvl_api")
def fixture_cvl_api(cvl_token: str):
    """Returns CVL Webservice"""
    api_url = os.environ["CVL_API_URL"]
    verify_ssl = os.environ.get("CVL_API_VERIFY_SSL")
    yield CVLAPI(token=cvl_token, base_url=api_url, verify_ssl=verify_ssl)


def test_cvlapi_post_pgx(cvl_api: CVLAPI):
    """Test postin a bare minimum PGX file"""
    data = {
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "revision_number": "2.1.2",
    }
    response = cvl_api.post("PGX", "s3://fake/s3/path", **data)
    assert response == {"success": True, "content": "Upload success"}


def test_cvlapi_post_hdr(cvl_api: CVLAPI):
    """Test postin a bare minimum HDR file"""
    data = {
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "revision_number": "2.1.2",
    }
    response = cvl_api.post("HDR", "s3://fake/s3/path", **data)
    assert response == {"success": True, "content": "Upload success"}


@pytest.mark.xfail(reason="Not implemented in CVL_API yet")
def test_cvlapi_post_w1il_hdr(cvl_api: CVLAPI):
    """Test posting a bare minimum W1IL record succeds"""
    data = {
        "biobank_id": "test-biobank-id-001",
        "wgs_sample_external_id": "test-wgs_sample_external_id-001",
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "vcf_raw_path": "some-vcf_raw_path",
        "vcf_raw_index_path": "some-vcf_raw_index_path",
        "vcf_raw_md5_path": "some-vcf_raw_md5_path",
        "cram_name": "some-cram_name",
        "sex_at_birth": "F",
        "ny_flag": "Y",
        "genome_center": "BCM",
        "consent_for_gror": "Y",
        "genome_type": "test",
        "informing_loop_hdr": "Y",
        "aou_hdr_coverage": "test",
        "contamination": "test",
    }
    response = cvl_api.post("W1IL_HDR", "s3://fake/s3/path", data=[data])
    assert response == {"success": True, "content": "Upload success"}


@pytest.mark.xfail(reason="Not implemented in CVL_API yet")
def test_cvlapi_post_w1il_pgx(cvl_api: CVLAPI):
    """Test posting a bare minimum W1IL record succeds"""
    data = {
        "biobank_id": "test-biobank-id-001",
        "wgs_sample_external_id": "test-wgs_sample_external_id-001",
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "vcf_raw_path": "some-vcf_raw_path",
        "vcf_raw_index_path": "some-vcf_raw_index_path",
        "vcf_raw_md5_path": "some-vcf_raw_md5_path",
        "cram_name": "some-cram_name",
        "sex_at_birth": "F",
        "ny_flag": "Y",
        "genome_center": "BCM",
        "consent_for_gror": "Y",
        "genome_type": "test",
        "informing_loop_pgx": "Y",
        "aou_hdr_coverage": "test",
        "contamination": "test",
    }
    response = cvl_api.post("W1IL_PGX", "s3://fake/s3/path", data=[data])
    assert response == {"success": True, "content": "Upload success"}


def test_cvlapi_post_w2w(cvl_api: CVLAPI):
    """Test posting a bare minimum W2W record succeds"""
    data = {
        "biobank_id": "test-biobank-id-001",
        "wgs_sample_external_id": "test-wgs_sample_external_id-001",
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "date_of_consent_removal": "2020-09-25T18:50:43.766355+00:00",
    }
    response = cvl_api.post("W2W", "s3://fake/s3/path", data=[data])
    assert response == {"success": True, "content": "Upload success"}


def test_cvlapi_post_w2sc(cvl_api: CVLAPI):
    """Test posting a bare minimum W2SC record succeds"""
    data = {
        "biobank_id": "test-biobank-id-001",
        "wgs_sample_external_id": "test-wgs_sample_external_id-001",
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
    }
    response = cvl_api.post("W2SC", "s3://fake/s3/path", data=[data])
    assert response == {"success": True, "content": "Upload success"}


def test_cvlapi_post_w3ns(cvl_api: CVLAPI):
    """Test posting a bare minimum W3NS record succeeds"""
    data = {
        "biobank_id": "test-biobank-id-001",
        "wgs_sample_external_id": "test-wgs_sample_external_id-001",
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "unavailable_reason": "test some reason",
    }
    response = cvl_api.post("W3NS", "s3://fake/s3/path", data=[data])
    assert response == {"success": True, "content": "Upload success"}


def test_cvlapi_post_w3ss(cvl_api: CVLAPI):
    """Test posting a bare minimum W3SS record succeds"""
    data = {
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "wgs_sample_external_id": "test-wgs_sample_external_id-001",
        "version": "V2",
        "package_id": "some-package",
        "biobankid_sampleid": "test-biobank-id-001_test-sample-id-001",
        "box_storageunit_id": "test-box-storageunit-id-001",
        "box_id_plate_id": "test-box_id_plate_id_001",
        "well_position": "A01",
        "cvl_sample_external_id": "test-cvl_sample_external_id-001",
        "cvl_sample_internal_id": "test-cvl_sample_internal_id-001",
        "parent_sample_id": "test-parent-sample-id-001",
        "collection_tubeid": "test-collection-tubeid-001",
        "matrix_id": "test-matrix-id-001",
        "collection_date": "2021-06-16T12:45:55Z",
        "biobank_id": "test-biobank-id-001",
        "sex_at_birth": "F",
        "age": "",
        "ny_state": "Y",
        "sample_type": "test",
        "treatments": "TE",
        "quantity_ul": "111",
        "total_concentration_ng_ul": "11",
        "total_dna_ng": "11",
        "visit_description": "test",
        "sample_sources": "Blood",
        "study": "test",
        "tracking_number": "test",
        "contact": "test",
        "email": "test",
        "study_pi": "test",
        "site_name": "test",
        "genome_type": "test",
        "failure_mode": "test",
        "failure_mode_desc": "test",
    }
    response = cvl_api.post("W3SS", "s3://fake/s3/path", data=[data])
    assert response == {"success": True, "content": "Upload success"}


def test_cvlapi_post_w5nf(cvl_api: CVLAPI):
    """Test posting a bare minimum W5NF record succeds"""
    data = {
        "biobank_id": "test-biobank_id-001",
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "wgs_sample_external_id": "test-wgs_sample_external_id-001",
        "request_reason": "test-request_reason-001",
        "request_reason_free": "test-request_reason_free-001",
        "health_related_data_file_name": "test-health_related_data_file_name-001",
        "clinical_analysis_type": "test-clinical_analysis_type-001",
    }
    response = cvl_api.post("W5NF", "s3://fake/s3/path", data=[data])
    assert response == {"success": True, "content": "Upload success"}


def test_cvlapi_post_w3sc(cvl_api: CVLAPI):
    """Test postin a bare minimum W3SC file"""
    data = {
        "biobank_id": "test-biobank_id-001",
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "wgs_sample_external_id": "test-wgs_sample_external_id-001",
        "cvl_secondary_conf_failure": "Test",
    }
    response = cvl_api.post("W3SC", "s3://fake/s3/path", data=[data])
    assert response == {"success": True, "content": "Upload success"}


@pytest.mark.xfail(reason="Not implemented in CVL_API yet")
def test_cvlapi_post_w4wr_hdr(cvl_api: CVLAPI):
    """Test postin a bare minimum W4WR_PGX file"""
    data = {
        "biobank_id": "test-biobank_id-001",
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "wgs_sample_external_id": "test-wgs_sample_external_id-001",
        "health_related_data_file_name": "test-health_related_data_file_name-001",
        "clinical_analysis_type": "HDRV1",
    }
    response = cvl_api.post("W4WR_HDR", "s3://fake/s3/path", data=[data])
    assert response == {"success": True, "content": "Upload success"}


@pytest.mark.xfail(reason="Not implemented in CVL_API yet")
def test_cvlapi_post_w4wr_pgx(cvl_api: CVLAPI):
    """Test postin a bare minimum W4WR_PGX file"""
    data = {
        "biobank_id": "test-biobank_id-001",
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "wgs_sample_external_id": "test-wgs_sample_external_id-001",
        "health_related_data_file_name": "test-health_related_data_file_name-001",
        "clinical_analysis_type": "PGXV1",
    }
    response = cvl_api.post("W4WR_PGX", "s3://fake/s3/path", data=[data])
    assert response == {"success": True, "content": "Upload success"}


def test_cvlapi_post_w6d(cvl_api: CVLAPI):
    """Test posting a bare minimum W6D record succeds"""
    data = {
        "biobank_id": "test-biobank-id-001",
        "wgs_sample_external_id": "test-wgs_sample_external_id-001",
        "wgs_sample_internal_id": "test-wgs_sample_internal_id-001",
        "date_of_consent_removal": "2020-09-25T18:50:43.766355+00:00",
    }
    response = cvl_api.post("W6D", "s3://fake/s3/path", data=[data])
    assert response == {"success": True, "content": "Upload success"}


def test_cvl_api_get_wgs_sample_internal_id_success(cvl_api: CVLAPI):
    """Test that get returns wgs_sample_internal_id as expected"""
    response = cvl_api.get_wgs_sample_internal_id("test-wgs_sample_external_id-001")
    assert response == "test-wgs_sample_internal_id-001"


def test_cvl_api_get_wgs_sample_internal_id_failure(cvl_api: CVLAPI):
    """Test that get returns wgs_sample_internal_id raises an exception if
    - more than two internal ids return
    - no internal id is found
    """
    wgs_sample_external_id = "test-wgs_sample_external_id-002"
    with pytest.raises(HGSCWebServiceError) as err:
        cvl_api.get_wgs_sample_internal_id(wgs_sample_external_id)
    assert (
        err.value.message
        == f"Multiple wgs_sample_internal_ids were returned for {wgs_sample_external_id}"
    )
    wgs_sample_external_id = "test-wgs_sample_external_id-004"
    with pytest.raises(HGSCWebServiceError) as err:
        cvl_api.get_wgs_sample_internal_id(wgs_sample_external_id)
    assert (
        err.value.message
        == f"No wgs_sample_internal_id was returned for {wgs_sample_external_id}"
    )
