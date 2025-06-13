resource "aws_sqs_queue" "fbref_match_queue" {
  name_prefix = "${var.project_prefix}-${local.queue_prefix}-"
}