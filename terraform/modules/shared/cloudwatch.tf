resource "aws_cloudwatch_log_group" "fantasy-league-project-cw-log-group" {
  name              = "${var.project_prefix}-cw-log-group"
  retention_in_days = 14
}