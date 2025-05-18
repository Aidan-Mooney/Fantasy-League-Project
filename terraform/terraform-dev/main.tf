module "shared_bucket" {
  source = "../modules/shared"
  
}


module "extract" {
  source            = "../modules/extract"
  code_bucket       = module.shared_bucket.code_bucket_name
  project_directory = local.project_directory
}