output "code_bucket_name" {
  value = aws_s3_bucket.code_bucket.bucket
}


output "code_bucket_policy_arn" {
  value = aws_iam_policy.s3_code_policy.arn
}


output "processed_codes_arn" {
  value = aws_s3_bucket.fbref_fixture_tracker.arn
}


output "externals_layer_arn" {
  value = aws_lambda_layer_version.externals.arn
}


output "shared_utils_layer_arn" {
  value = aws_lambda_layer_version.shared_utils.arn
}