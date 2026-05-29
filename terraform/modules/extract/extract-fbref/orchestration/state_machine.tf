resource "aws_sfn_state_machine" "extract_fbref_state_machine" {
  name_prefix = "${var.project_prefix}-${local.state_machine_prefix}-"
  role_arn    = aws_iam_role.state_role.arn
  definition  = templatefile(
    "${var.project_directory}/state-machines/extract-fbref.asl.json", {
      sqs_input       = var.sqs_input_arn,
      sqs_output      = var.sqs_output_arn,
      extract_match   = var.extract_match_arn,
      get_match_codes = var.get_match_codes_arn
    }
  )
}