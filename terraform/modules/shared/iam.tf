data "aws_iam_policy_document" "s3_code_document" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.code_bucket.arn}/*"]
  }
}
