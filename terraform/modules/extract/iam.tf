resource "aws_iam_role" "extract_fixture_links_role" {
  name_prefix        = "role-${local.extract_fixture_links_name}"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_role_document.json
  description        = "IAM role used by '${local.extract_fixture_links_name}' lambda function."
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


data "aws_iam_policy_document" "extract_fixture_links_list_bucket_policy_document" {
  statement {
    actions   = ["s3:ListObjectV2"]
    resources = ["${var.processed_codes_bucket_arn}"]
  }
}


resource "aws_iam_policy" "extract_fixture_links_list_bucket_policy" {
  name_prefix = "list-processed-codes-policy-"
  policy      = data.aws_iam_policy_document.extract_fixture_links_list_bucket_policy_document.json
  description = "allows cloud service to access objects inside '${var.code_bucket.id}'."
}


resource "aws_iam_role_policy_attachment" "extract_fixture_links_code_policy" {
  role       = aws_iam_role.extract_fixture_links_role.name
  policy_arn = var.code_bucket_get_object_policy_arn
}


resource "aws_iam_role_policy_attachment" "extract_fixture_links_list_bucket_content_policy" {
  role       = aws_iam_role.extract_fixture_links_role.name
  policy_arn = aws_iam_policy.extract_fixture_links_list_bucket_policy.arn
}