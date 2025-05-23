locals {
  project_name = "fpl"
  stage = "dev"
}


locals {
  project_directory = "${path.module}/../.."
}


locals {
  python_runtime = "python3.12"
  timeout = 10
}