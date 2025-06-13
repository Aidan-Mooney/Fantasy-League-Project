resource "aws_lambda_function" "get_match_codes" {
  role                  = aws_iam_role.get_match_codes_role.arn
  function_name         = "${var.project_prefix}-${local.get_match_codes_name}-"
  source_code_hash      = data.archive_file.get_match_codes.output_base64sha256
  s3_bucket             = aws_s3_object.get_match_codes_file.bucket
  s3_key                = aws_s3_object.get_match_codes_file.id
  runtime               = var.python_runtime
  timeout               = var.timeout
  handler               = "get_match_codes.get_match_codes"
  layers                = [
    var.util_layer_arn,
    var.externals_arn,
  ]
  description           = "Lambda function for extracting fbref match codes that have not already been processed."
  environment {
    variables = { 
      PROC_TRACK_BUCKET = var.processed_codes_bucket_name
    }
  }
  logging_config {
    log_format  = "Text"
    log_group   = var.log_group_name
  }
}


resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn = aws_sqs_queue.sqs_queue_test.arn
  function_name    = aws_lambda_function.example.arn
}