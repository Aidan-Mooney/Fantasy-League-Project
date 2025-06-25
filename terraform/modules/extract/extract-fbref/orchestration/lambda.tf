resource "aws_lambda_function" "extract_template" {
  role          = aws_iam_role.extract_template_role.arn
  function_name = "${var.project_prefix}-${local.extract_template_prefix}-"
  s3_bucket     = aws_s3_object.extract_template_file.bucket
  s3_key        = aws_s3_object.extract_template_file.id
  runtime       = var.python_runtime
  timeout       = var.timeout
  handler       = "extract_template.extract_template"
  description   = "Lambda function for extracting."
  environment {
    variables = { 
      STEPFUNCTION_NAME = ""
    }
  }
  logging_config {
    log_format  = "Text"
    log_group   = var.log_group_name
  }
}