data "aws_iam_policy_document" "s3_code_document" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.code_bucket.arn}/*"]
  }
}


resource "aws_iam_policy" "s3_code_policy" {
  name_prefix = "${var.project_prefix}-s3-code-policy-"
  policy      = data.aws_iam_policy_document.s3_code_document.json
  description = "allows cloud service to access objects inside '${aws_s3_bucket.code_bucket.id}'."
}


data "aws_iam_policy_document" "get_template_policy_document" {
  statement {
    actions = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.template_bucket.arn}/*"]
  }
}


resource "aws_iam_policy" "get_template_policy" {
  name_prefix = "${var.project_prefix}-get-template-policy-"
  policy      = data.aws_iam_policy_document.get_template_policy_document.json
  description = "allows cloud service to retrieve items from the template bucket."
}