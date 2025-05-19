resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = local.code_bucket_prefix
  tags = {
    purpose = "holds python code for lambda files."
  }
}


resource "aws_s3_bucket" "fbref_fixture_tracker" {
  bucket_prefix = local.fbref_fixture_tracker_prefix
  tags = {
    step = "extract"
    purpose = "hold codes of matches that have been processed."
  }
}


data "archive_file" "externals"{
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${var.project_directory}/layers/externals/python"
  output_path      = "${var.project_directory}/packages/externals.zip"
}


data "archive_file" "shared_utils"{
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${var.project_directory}/layers/shared_utils/python"
  output_path      = "${var.project_directory}/packages/shared_utils.zip"
}


resource "aws_s3_object" "externals_file" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "shared/externals.zip"
  source = "${var.project_directory}/packages/externals.zip"
  etag   = filemd5(data.archive_file.externals.output_path)
}


resource "aws_s3_object" "shared_utils_file" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "shared/shared_utils.zip"
  source = "${var.project_directory}/packages/shared_util.zip"
  etag   = filemd5(data.archive_file.shared_util.output_path)
}