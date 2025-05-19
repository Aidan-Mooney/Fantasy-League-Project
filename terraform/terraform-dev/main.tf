module "shared" {
  source            = "../modules/shared"
  project_directory = local.project_directory
  python_runtime    = local.python_runtime
}


module "extract" {
  source                            = "../modules/extract"
  project_directory                 = local.project_directory
  code_bucket                       = module.shared.code_bucket_name
  code_bucket_get_object_policy_arn = module.shared.code_bucket_policy_arn
  python_runtime                    = local.python_runtime
  timeout                           = local.timeout
  processed_codes_bucket_arn        = module.shared.processed_codes_arn
  externals_arn                     = module.shared.externals_layer_arn
  util_layer_arn                    = module.shared.util_layer_layer_arn
}