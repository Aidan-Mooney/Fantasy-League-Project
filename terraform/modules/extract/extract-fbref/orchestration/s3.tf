data "archive_file" "extract_template" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${var.project_directory}/src/extract/extract_fbref/extract_template.py"
  output_path      = "${var.project_directory}/packages/extract_template.zip"
}


resource "aws_s3_object" "extract_template_file" {
  bucket = var.code_bucket
  key    = "extract/extract_fbref/extract_template.zip"
  source = data.archive_file.extract_template.output_path
  etag   = data.archive_file.extract_template.output_md5
}