module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.16.0"

  # Name and CIDR block for the VPC
  name = var.vpc_name
  cidr = var.vpc_cidr

  # Availability zones and subnets
  azs             = var.availability_zones
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  # Enable NAT Gateway for internet access from private subnets
  enable_nat_gateway = true
  single_nat_gateway = true

  # Resource tags for organization and management
  tags = {
    Terraform   = "true"
    Environment = var.environment
  }
}
