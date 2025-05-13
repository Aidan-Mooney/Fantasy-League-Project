resource "aws_s3_bucket" "fbref_fixture_tracker" {
  bucket_prefix = var.fbref_fixture_tracker-prefix
  tags = {
    step = "extract"
    purpose = "hold codes of matches that have been processed."
  }
}