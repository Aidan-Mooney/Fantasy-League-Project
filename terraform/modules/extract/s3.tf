data "archive_file" "extract_fixture_links" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${var.project_directory}/src/extract_fixtures/get_fixture_links.py"
  output_path      = "${var.project_directory}/packages/get_fixture_links.zip"
}


resource "aws_s3_object" "extract_fixture_links_lambda_file" {
  bucket = var.code_bucket
  key    = "extract/get_fixture_links.zip"
  source = "${var.project_directory}/packages/get_fixture_links.zip"
  etag   = filemd5(data.archive_file.extract_fixture_links.output_path)
}

