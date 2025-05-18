module "shared_bucket" {
  source = "../modules/shared"
  
}


module "extract" {
  source       = "../modules/extract"
  code_bucket  = module.shared_bucket.code_bucket_name
  package_path = var.package_path
}