locals {
  stage = "prod"
}


locals {
  project_directory = "${path.module}/../.."
}


locals {
  python_runtime = "python3.12"
  timeout = 10
}