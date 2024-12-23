terraform {
  backend "s3" {
    bucket         = "yafit-technion-cicd-13579"
    key            = "terraform/state/dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}
