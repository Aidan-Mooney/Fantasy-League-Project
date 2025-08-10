resource "aws_ssm_parameter" "step_function_arn" {
  name  = "/${var.project_prefix}/extract-fbref-stepfunction/arn"
  type  = "String"
  value = aws_sfn_state_machine.extract_fbref_state_machine.arn
}