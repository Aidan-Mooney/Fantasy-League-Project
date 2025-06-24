resource "aws_iam_role" "sqs_input_role" {
  name_prefix        = "${var.project_prefix}-role-${local.input_prefix}"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_role_document.json
  description        = "IAM role used by '${local.input_prefix}' lambda function."
}


resource "aws_iam_role" "sqs_output_role" {
  name_prefix        = "${var.project_prefix}-role-${local.output_prefix}"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_role_document.json
  description        = "IAM role used by '${local.output_prefix}' lambda function."
}


data "aws_iam_policy_document" "assume_lambda_role_document" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}


data "aws_iam_policy_document" "sqs_send_message_policy_document" {
  statement {
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.fbref_match_queue.arn]
  }
}


data "aws_iam_policy_document" "sqs_receive_and_delete_policy_document" {
  statement {
    actions   = ["sqs:ReceiveMessage","sqs:DeleteMessage"]
    resources = [aws_sqs_queue.fbref_match_queue.arn]
  }
}


resource "aws_iam_policy" "sqs_send_message_policy" {
  name_prefix = "${var.project_prefix}-sqs-send-message-policy-"
  policy      = data.aws_iam_policy_document.sqs_send_message_policy_document.json
  description = "allows cloud service to send messages to the extract-fbref queue."
}


resource "aws_iam_policy" "sqs_receive_and_delete_policy" {
  name_prefix = "${var.project_prefix}-sqs-send-message-policy-"
  policy      = data.aws_iam_policy_document.sqs_receive_and_delete_policy_document.json
  description = "allows cloud service to receive and delete messages in the extract-fbref queue."
}


resource "aws_iam_role_policy_attachment" "sqs_send_message_policy_attachment" {
  role       = aws_iam_role.sqs_input_role.name
  policy_arn = aws_iam_policy.sqs_send_message_policy.arn
}


resource "aws_iam_role_policy_attachment" "sqs_receive_and_delete_policy_attachment" {
  role       = aws_iam_role.sqs_output_role.name
  policy_arn = aws_iam_policy.sqs_receive_and_delete_policy.arn
}


resource "aws_iam_role_policy_attachment" "get_match_codes_code_policy" {
  role       = aws_iam_role.sqs_input_role.name
  policy_arn = var.code_bucket_get_object_policy_arn
}


resource "aws_iam_role_policy_attachment" "get_match_codes_code_policy" {
  role       = aws_iam_role.sqs_output_role.name
  policy_arn = var.code_bucket_get_object_policy_arn
}