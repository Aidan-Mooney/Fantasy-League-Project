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

