from gift_wrap import rclone


def test_convert_cloud_path():
    """Test that a cloud path is correctly converted to the
    expected rclone format"""
    cloud_path = "s3://bucket_name/prefix/fake.csv"
    result = rclone.convert_cloud_path(cloud_path)
    assert result == "s3:bucket_name/prefix/fake.csv"
