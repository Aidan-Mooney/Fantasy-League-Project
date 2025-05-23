resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = "${var.project_prefix}-${local.code_bucket_prefix}"
  tags = {
    purpose = "holds python code for lambda files."
  }
}


resource "aws_s3_bucket" "fbref_fixture_tracker" {
  bucket_prefix = "${var.project_prefix}-${local.fbref_fixture_tracker_prefix}"
  tags = {
    step = "extract"
    purpose = "hold codes of matches that have been processed."
  }
}


data "archive_file" "externals"{
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${var.project_directory}/layers/externals"
  output_path      = "${var.project_directory}/packages/externals.zip"
}


data "archive_file" "shared_utils"{
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${var.project_directory}/layers/shared_utils"
  output_path      = "${var.project_directory}/packages/shared_utils.zip"
}


resource "aws_s3_object" "externals_file" {
  bucket     = aws_s3_bucket.code_bucket.bucket
  key        = "shared/externals.zip"
  source     = data.archive_file.externals.output_path
  etag       = data.archive_file.externals.output_md5
}


resource "aws_s3_object" "shared_utils_file" {
  bucket     = aws_s3_bucket.code_bucket.bucket
  key        = "shared/shared_utils.zip"
  source     = data.archive_file.shared_utils.output_path
  etag       = data.archive_file.shared_utils.output_md5
}