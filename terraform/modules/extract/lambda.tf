resource "aws_lambda_function" "ingest_lambda_function" {
  role                  = aws_iam_role.extract_fixture_links_role.arn
  function_name         = local.extract_fixture_links_name
  source_code_hash      = data.archive_file.extract_fixture_links.output_base64sha256
  s3_bucket             = var.code_bucket
  s3_key                = aws_s3_object.extract_fixture_links_lambda_file.id
  runtime               = var.python_runtime
  timeout               = var.timeout
  handler               = "${locals.extract_fixture_links_name}.lambda_handler"
  description           = "Lambda function for extracting fbref match codes that have not already been processed."
  environment {
    variables = { 
      EXTRACT-BUCKET = var.processed_codes_bucket_arn
    }
  }
}