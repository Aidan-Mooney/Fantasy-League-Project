resource "aws_lambda_function" "extract_match" {
  role                  = aws_iam_role.extract_match_role.arn
  function_name         = "${var.project_prefix}-${local.extract_match_name}"
  source_code_hash      = data.archive_file.extract_match.output_base64sha256
  s3_bucket             = aws_s3_object.extract_match_file.bucket
  s3_key                = aws_s3_object.extract_match_file.id
  runtime               = var.python_runtime
  timeout               = var.timeout
  handler               = "extract_match.extract_match"
  layers                = [
    var.util_layer_arn,
    var.externals_arn,
  ]
  description           = "Lambda function for extracting data from a specific fbref match."
  environment {
    variables = { 
      PROC_TRACK_BUCKET = var.processed_codes_bucket_name
      EXTRACT_BUCKET    = var.extract_bucket_name
      TEMPLATE_BUCKET   = var.template_bucket_name
    }
  }
  logging_config {
    log_format  = "Text"
    log_group   = var.log_group_name
  }
}
}