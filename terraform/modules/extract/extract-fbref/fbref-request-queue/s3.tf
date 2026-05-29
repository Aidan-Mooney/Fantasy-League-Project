data "archive_file" "sqs_input" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${var.project_directory}/src/extract/extract_fbref/sqs_input.py"
  output_path      = "${var.project_directory}/packages/sqs_input.zip"
}


resource "aws_s3_object" "sqs_input_file" {
  bucket = var.code_bucket
  key    = "extract/extract_fbref/sqs_input.zip"
  source = data.archive_file.sqs_input.output_path
  etag   = data.archive_file.sqs_input.output_md5
}


data "archive_file" "sqs_output" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${var.project_directory}/src/extract/extract_fbref/sqs_output.py"
  output_path      = "${var.project_directory}/packages/sqs_output.zip"
}


resource "aws_s3_object" "sqs_output_file" {
  bucket = var.code_bucket
  key    = "extract/extract_fbref/sqs_output.zip"
  source = data.archive_file.sqs_output.output_path
  etag   = data.archive_file.sqs_output.output_md5
}