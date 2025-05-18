data "archive_file" "extract_fixture_links" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${var.src_path}/extract_fixtures/get_fixture_links.py"
  output_path      = "${var.package_path}/get_fixture_links.zip"
}


resource "aws_s3_object" "extract_fixture_links_lambda_file" {
  bucket = var.code_bucket.bucket
  key    = "extract/get_fixture_links.zip"
  source = "${var.package_path}/get_fixture_links.zip"
  etag   = filemd5(data.archive_file.extract_fixture_links.output_path)
}

