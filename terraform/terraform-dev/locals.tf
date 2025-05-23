locals {
  project_name = "Fantasy-League-Project"
  stage = "DEV"
}


locals {
  project_directory = "${path.module}/../.."
}


locals {
  python_runtime = "python3.12"
  timeout = 10
}