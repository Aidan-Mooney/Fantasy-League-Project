resource "aws_iam_role" "state_role" {
  name_prefix        = "role-${local.state_machine_prefix}"
  assume_role_policy = data.aws_iam_policy_document.assume_state_role_document.json
  description        = "IAM role used by '${local.state_machine_prefix}' state machine."
}


data "aws_iam_policy_document" "assume_state_role_document" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }
  }
}


data "aws_iam_policy_document" "invoke_lambdas_document" {
  statement {
    actions   = [
      "lambda:InvokeFunction"
    ]
    resources = [
      var.sqs_input_arn,
      var.sqs_output_arn,
      var.extract_match_arn,
      var.get_match_codes_arn
    ]
  }
}


resource "aws_iam_policy" "invoke_lambdas_policy" {
  name_prefix = "invoke-lambda-policy-for-${local.state_machine_prefix}-state-machine."
  policy      = data.aws_iam_policy_document.invoke_lambdas_document.json
  description = "allows state machine to envoke lambda func it contains."
}


resource "aws_iam_role_policy_attachment" "invoke_lambdas_policy_attachment" {
  role       = aws_iam_role.state_role.name
  policy_arn = aws_iam_policy.invoke_lambdas_policy.arn
}