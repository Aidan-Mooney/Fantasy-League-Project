resource "aws_lambda_layer_version" "externals" {
  layer_name          = "externals"
  compatible_runtimes = [var.python_runtime]
  s3_bucket           = aws_s3_object.externals_file.bucket
  s3_key              = aws_s3_object.externals_file.key
  source_code_hash    = data.archive_file.externals.output_base64sha256
  description         = "Lambda layer containing project external requirements."
}

resource "aws_lambda_layer_version" "shared_utils" {
  layer_name          = "shared_utils"
  compatible_runtimes = [var.python_runtime]
  s3_bucket           = aws_s3_object.shared_utils_file.bucket
  s3_key              = aws_s3_object.shared_utils_file.key
  source_code_hash    = data.archive_file.shared_utils.output_base64sha256
  description         = "Lambda layer containing project shared utils."
}