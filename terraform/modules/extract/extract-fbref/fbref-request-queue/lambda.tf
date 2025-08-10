resource "aws_lambda_function" "sqs_input" {
  role            = aws_iam_role.sqs_input_role.arn
  function_name   = "${var.project_prefix}-${local.input_prefix}-"
  s3_bucket       = aws_s3_object.sqs_input_file.bucket
  s3_key          = aws_s3_object.sqs_input_file.id
  runtime         = var.python_runtime
  timeout         = var.timeout
  handler         = "sqs_input.sqs_input"
  description     = "Lambda function for adding messages to the queue: ${aws_sqs_queue.fbref_match_queue.id}."
  environment {
    variables = { 
      FBREF_QUEUE = aws_sqs_queue.fbref_match_queue.id
    }
  }
  logging_config {
    log_format  = "Text"
    log_group   = var.log_group_name
  }
}


resource "aws_lambda_function" "sqs_output" {
  role            = aws_iam_role.sqs_output_role.arn
  function_name   = "${var.project_prefix}-${local.output_prefix}-"
  s3_bucket       = aws_s3_object.sqs_output_file.bucket
  s3_key          = aws_s3_object.sqs_output_file.id
  runtime         = var.python_runtime
  timeout         = var.timeout
  handler         = "sqs_output.sqs_output"
  description     = "Lambda function for receiving and deleting messages from the queue: ${aws_sqs_queue.fbref_match_queue.id}."
  environment {
    variables = { 
      FBREF_QUEUE = aws_sqs_queue.fbref_match_queue.id
    }
  }
  logging_config {
    log_format  = "Text"
    log_group   = var.log_group_name
  }
}