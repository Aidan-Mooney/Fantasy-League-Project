module "shared" {
  source            = "../modules/shared"
  project_prefix    = "${local.project_name}-${local.stage}"
  project_directory = local.project_directory
  python_runtime    = local.python_runtime
}


module "get-match-codes" {
  source                            = "../modules/extract/extract-fbref/get-match-codes"
  project_prefix                    = "${local.project_name}-${local.stage}"
  project_directory                 = local.project_directory
  code_bucket                       = module.shared.code_bucket_name
  code_bucket_get_object_policy_arn = module.shared.code_bucket_policy_arn
  python_runtime                    = local.python_runtime
  timeout                           = local.timeout
  processed_codes_bucket_name       = module.shared.processed_codes_name
  processed_codes_bucket_arn        = module.shared.processed_codes_arn
  externals_arn                     = module.shared.externals_layer_arn
  util_layer_arn                    = module.shared.shared_utils_layer_arn
  log_group_name                    = module.shared.log_group_name
}


module "extract-match" {
  source                            = "../modules/extract/extract-fbref/extract-match"
  project_prefix                    = "${local.project_name}-${local.stage}"
  project_directory                 = local.project_directory
  code_bucket                       = module.shared.code_bucket_name
  code_bucket_get_object_policy_arn = module.shared.code_bucket_policy_arn
  python_runtime                    = local.python_runtime
  timeout                           = local.timeout
  processed_codes_bucket_name       = module.shared.processed_codes_name
  processed_codes_bucket_arn        = module.shared.processed_codes_arn
  template_bucket_name              = module.shared.template_bucket_name
  template_bucket_policy_arn        = module.shared.template_bucket_policy_arn
  extract_bucket_name               = module.shared.extract_bucket_name
  extract_bucket_arn                = module.shared.extract_bucket_arn
  externals_arn                     = module.shared.externals_layer_arn
  util_layer_arn                    = module.shared.shared_utils_layer_arn
  log_group_name                    = module.shared.log_group_name
}