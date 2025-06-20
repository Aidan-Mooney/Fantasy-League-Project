output "code_bucket_name" {
  value = aws_s3_bucket.code_bucket.bucket
}


output "code_bucket_policy_arn" {
  value = aws_iam_policy.s3_code_policy.arn
}


output "template_bucket_name" {
  value = aws_s3_bucket.template_bucket.bucket
}


output "template_bucket_policy_arn" {
  value = aws_iam_policy.get_template_policy.arn
}


output processed_codes_name {
  value = aws_s3_bucket.fbref_fixture_tracker.id
}


output "processed_codes_arn" {
  value = aws_s3_bucket.fbref_fixture_tracker.arn
}


output "extract_bucket_name" {
  value = aws_s3_bucket.fbref_extract_bucket.id
}


output  "extract_bucket_arn" {
  value = aws_s3_bucket.fbref_extract_bucket.arn
}


output "externals_layer_arn" {
  value = aws_lambda_layer_version.externals.arn
}


output "shared_utils_layer_arn" {
  value = aws_lambda_layer_version.shared_utils.arn
}


output "log_group_name" {
  value = aws_cloudwatch_log_group.fantasy-league-project-cw-log-group.name
}