resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = var.code_bucket_prefix
  tags = {
    purpose = "holds python code for lambda files."
  }
}


resource "aws_s3_bucket" "fbref_fixture_tracker" {
  bucket_prefix = var.fbref_fixture_tracker_prefix
  tags = {
    step = "extract"
    purpose = "hold codes of matches that have been processed."
  }
}