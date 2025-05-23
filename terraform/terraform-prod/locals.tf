locals {
  project_name = "FPL"
  stage = "PROD"
}



locals {
  project_directory = "${path.module}/../.."
}


locals {
  python_runtime = "python3.12"
  timeout = 10
}