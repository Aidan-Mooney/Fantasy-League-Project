module "get_match_codes" {
  source                            = "./get-match-codes"
  project_prefix                    = var.project_prefix
  project_directory                 = var.project_directory
  code_bucket                       = var.code_bucket
  code_bucket_get_object_policy_arn = var.code_bucket_get_object_policy_arn
  python_runtime                    = var.python_runtime
  timeout                           = var.timeout
  processed_codes_bucket_name       = var.processed_codes_bucket_name
  processed_codes_bucket_arn        = var.processed_codes_bucket_arn
  externals_arn                     = var.externals_arn
  util_layer_arn                    = var.util_layer_arn
  log_group_name                    = var.log_group_name
}


module "extract_match" {
  source                            = "./extract-match"
  project_prefix                    = var.project_prefix
  project_directory                 = var.project_directory
  code_bucket                       = var.code_bucket
  code_bucket_get_object_policy_arn = var.code_bucket_get_object_policy_arn
  python_runtime                    = var.python_runtime
  timeout                           = var.timeout
  processed_codes_bucket_name       = var.processed_codes_bucket_name
  processed_codes_bucket_arn        = var.processed_codes_bucket_arn
  template_bucket_name              = var.template_bucket_name
  template_bucket_policy_arn        = var.template_bucket_policy_arn
  extract_bucket_name               = var.extract_bucket_name
  extract_bucket_arn                = var.extract_bucket_arn
  externals_arn                     = var.externals_arn
  util_layer_arn                    = var.util_layer_arn
  log_group_name                    = var.log_group_name
}


module "fbref_request_queue" {
  source                            = "./fbref-request-queue"
  project_prefix                    = var.project_prefix
  project_directory                 = var.project_directory
  code_bucket                       = var.code_bucket
  code_bucket_get_object_policy_arn = var.code_bucket_get_object_policy_arn
  python_runtime                    = var.python_runtime
  timeout                           = var.timeout
  log_group_name                    = var.log_group_name
}


module "orchestration" {
  source              = "./orchestration"
  project_prefix      = var.project_prefix
  project_directory   = var.project_directory
  sqs_input_arn       = module.fbref_request_queue.sqs_input_func_arn
  sqs_output_arn      = module.fbref_request_queue.sqs_input_func_arn
  extract_match_arn   = module.extract_match.extract_match_func_arn
  get_match_codes_arn = module.get_match_codes.get_match_codes_func_arn
}