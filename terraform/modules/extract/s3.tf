data "archive_file" "get_match_codes" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${var.project_directory}/src/extract/extract_fbref/get_match_codes.py"
  output_path      = "${var.project_directory}/packages/get_match_codes.zip"
}


resource "aws_s3_object" "get_match_codes_file" {
  bucket = var.code_bucket
  key    = "extract/extract_fbref/get_match_codes.zip"
  source = data.archive_file.get_match_codes.output_path
  etag   = data.archive_file.get_match_codes.output_md5
}


data "archive_file" "extract_match" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${var.project_directory}/src/extract/extract_fbref/extract_match.py"
  output_path      = "${var.project_directory}/packages/extract_match.zip"
}


resource "aws_s3_object" "extract_match_file" {
  bucket = var.code_bucket
  key    = "extract/extract_fbref/extract_match.zip"
  source = data.archive_file.extract_match.output_path
  etag   = data.archive_file.extract_match.output_md5
}