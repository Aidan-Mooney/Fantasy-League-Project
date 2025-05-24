resource "aws_iam_role" "get_match_codes_role" {
  name_prefix        = "${var.project_prefix}-role-${local.get_match_codes_name}"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_role_document.json
  description        = "IAM role used by '${local.get_match_codes_name}' lambda function."
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


data "aws_iam_policy_document" "get_match_codes_list_bucket_policy_document" {
  statement {
    actions   = ["s3:ListBucket"]
    resources = ["${var.processed_codes_bucket_arn}"]
  }
}


resource "aws_iam_policy" "get_match_codes_list_bucket_policy" {
  name_prefix = "${var.project_prefix}-list-processed-codes-policy-"
  policy      = data.aws_iam_policy_document.get_match_codes_list_bucket_policy_document.json
  description = "allows cloud service to access objects inside the processed codes bucket."
}


resource "aws_iam_role_policy_attachment" "get_match_codes_code_policy" {
  role       = aws_iam_role.get_match_codes_role.name
  policy_arn = var.code_bucket_get_object_policy_arn
}


resource "aws_iam_role_policy_attachment" "get_match_codes_list_bucket_content_policy" {
  role       = aws_iam_role.get_match_codes_role.name
  policy_arn = aws_iam_policy.get_match_codes_list_bucket_policy.arn
}