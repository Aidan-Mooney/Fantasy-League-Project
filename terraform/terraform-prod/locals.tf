locals {
  project_name = "Fantasy-League-Project"
  stage = "PROD"
}



locals {
  project_directory = "${path.module}/../.."
}


locals {
  python_runtime = "python3.12"
  timeout = 10
}