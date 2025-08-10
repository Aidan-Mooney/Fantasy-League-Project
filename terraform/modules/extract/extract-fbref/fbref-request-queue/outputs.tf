output "sqs_input_func_arn" {
  value = aws_lambda_function.sqs_input.arn
}


output "sqs_output_func_arn" {
  value = aws_lambda_function.sqs_output.arn
}