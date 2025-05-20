variable "project_directory" {
  type = string
}


variable "code_bucket" {
  description = "bucket for storing code"
}


variable "code_bucket_get_object_policy_arn" {
  type        = string
  description = "IAM policy to allow the lambda funcs to get their code from the code bucket."
}


variable "python_runtime" {
  type = string
}


variable "timeout" {
  type = number
}


variable "processed_codes_bucket_name" {
  type = string
}


variable "processed_codes_bucket_arn" {
  type = string
}


variable "util_layer_arn" {
  type = string
}


variable "externals_arn" {
  type = string
}


variable "log_group_name" {
  type = string
}