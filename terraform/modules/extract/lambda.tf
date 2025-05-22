resource "aws_lambda_function" "extract_fixture_links" {
  role                  = aws_iam_role.extract_fixture_links_role.arn
  function_name         = local.extract_fixture_links_name
  source_code_hash      = data.archive_file.extract_fixture_links.output_base64sha256
  s3_bucket             = aws_s3_object.extract_fixture_links_file.bucket
  s3_key                = aws_s3_object.extract_fixture_links_file.id
  runtime               = var.python_runtime
  timeout               = var.timeout
  handler               = "${local.extract_fixture_links_name}.lambda_handler"
  layers                = [
    var.util_layer_arn,
    var.externals_arn,
  ]
  description           = "Lambda function for extracting fbref match codes that have not already been processed."
  environment {
    variables = { 
      EXTRACT_BUCKET = var.processed_codes_bucket_name
    }
  }
  logging_config {
    log_format  = "Text"
    log_group   = var.log_group_name
  }
}