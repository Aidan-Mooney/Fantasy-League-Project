terraform {
  required_providers {
    aws = {
      source ="hashicorp/aws"
      version="~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "aid-moo-terraform-state"
    key            = "Fantasy-League-Project/dev/terraform.tfstate"
    region         = "eu-west-2"
  }
}

provider "aws"{
  region = "eu-west-2"
  default_tags {
    tags={
      ProjectName   = "Fantasy League Project"
      DeployedFrom  = "Terraform"
      Repository    = "Fantasy-League-Project"
      Environment   = "Dev"
    }
  }
}