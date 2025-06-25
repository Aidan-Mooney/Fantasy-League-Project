resource "aws_iam_role" "extract_template_role" {
  name_prefix        = "${var.project_prefix}-role-${local.extract_template_prefix}"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_role_document.json
  description        = "IAM role used by '${local.extract_template_prefix}' lambda function."
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


resource "aws_iam_role_policy_attachment" "extract_match_get_template_policy_attachment" {
  role       = aws_iam_role.extract_match_role.name
  policy_arn = var.template_bucket_policy_arn
}


resource "aws_iam_role_policy_attachment" "get_match_codes_code_policy" {
  role       = aws_iam_role.extract_match_role.name
  policy_arn = var.code_bucket_get_object_policy_arn
}