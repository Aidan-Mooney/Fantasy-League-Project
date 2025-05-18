module "shared_bucket" {
  source = "../modules/shared"
  
}


module "extract" {
  source                            = "../modules/extract"
  code_bucket                       = module.shared_bucket.code_bucket_name
  code_bucket_get_object_policy_arn = module.shared_bucket.code_bucket_policy_arn
  processed_codes_bucket_arn        = module.shared_bucket.processed_codes_arn
  project_directory                 = local.project_directory
  python_runtime                    = local.runtime
  timeout                           = local.timeout
}