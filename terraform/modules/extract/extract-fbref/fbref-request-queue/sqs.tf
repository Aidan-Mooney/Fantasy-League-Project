resource "aws_sqs_queue" "fbref_match_queue" {
  name                        = "${var.project_prefix}-${local.queue_prefix}.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
}