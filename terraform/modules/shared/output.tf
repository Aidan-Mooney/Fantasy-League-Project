output "code_bucket_name" {
  value = aws_s3_bucket.code_bucket.bucket
}


output "code_bucket_policy_arn" {
  value = data.aws_iam_policy_document.s3_code_document.arn
}


output "processed_codes_arn" {
  value = aws_s3_bucket.fbref_fixture_tracker.arn
}