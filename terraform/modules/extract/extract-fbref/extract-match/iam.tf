resource "aws_iam_role" "extract_match_role" {
  name_prefix        = "${var.project_prefix}-role-${local.extract_match_name}"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_role_document.json
  description        = "IAM role used by '${local.extract_match_name}' lambda function."
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


data "aws_iam_policy_document" "extract_match_put_object_policy_document" {
  statement {
    actions   = ["s3:PutObject"]
    resources = ["${var.processed_codes_bucket_arn}/*","${var.extract_bucket_arn}/*"]
  }
}


resource "aws_iam_policy" "extract_match_put_object_policy" {
  name_prefix = "${var.project_prefix}-extract-match-put-object-policy-"
  policy      = data.aws_iam_policy_document.extract_match_put_object_policy_document.json
  description = "allows cloud service to put objects into the processed codes bucket and the extract bucket."
}


resource "aws_iam_role_policy_attachment" "extract_match_put_object_policy_attachment" {
  role       = aws_iam_role.extract_match_role.name
  policy_arn = aws_iam_policy.extract_match_put_object_policy.arn
}


resource "aws_iam_role_policy_attachment" "extract_match_get_template_policy_attachment" {
  role       = aws_iam_role.extract_match_role.name
  policy_arn = var.template_bucket_policy_arn
}


resource "aws_iam_role_policy_attachment" "get_match_codes_code_policy" {
  role       = aws_iam_role.extract_match_role.name
  policy_arn = var.code_bucket_get_object_policy_arn
}