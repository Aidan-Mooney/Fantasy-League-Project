variable "project_prefix" {
  type = string
}


variable "project_directory" {
  type = string
}


variable "python_runtime" {
  type = string
}


variable "timeout" {
  type = number
}


variable "code_bucket" {
  description = "bucket for storing code"
}


variable "code_bucket_get_object_policy_arn" {
  type        = string
  description = "IAM policy to allow the lambda funcs to get their code from the code bucket."
}


variable "log_group_name" {
  type = string
}
