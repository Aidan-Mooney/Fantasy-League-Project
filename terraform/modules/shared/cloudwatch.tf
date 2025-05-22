resource "aws_cloudwatch_log_group" "fantasy-league-project-cw-log-group" {
  name              = "fantasy-league-project-${stage}-cw-log-group"
  retention_in_days = 14
}