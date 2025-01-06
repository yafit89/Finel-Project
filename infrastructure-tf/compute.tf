module "kind_cluster_instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"

  name                    = "kind-cluster"
  instance_type           = "t3.medium"
  key_name                = var.key_name
  monitoring              = true
  vpc_security_group_ids  = [aws_security_group.kind_cluster_sg.id]
  subnet_id               = element(module.vpc.public_subnets, 0)
  associate_public_ip_address = true

  tags = {
    Terraform   = "true"
    Environment = var.environment
    Project     = var.project_name
  }
}

# EBS Volume for MySQL
resource "aws_ebs_volume" "mysql_volume" {
  availability_zone = element(var.availability_zones, 0) # Select the first AZ
  size              = var.mysql_volume_size
  tags = {
    Name = "MySQL-Volume"
  }
}

# Attach EBS Volume to kind_cluster_instance
resource "aws_volume_attachment" "mysql_attachment" {
  instance_id = module.kind_cluster_instance.id
  volume_id   = aws_ebs_volume.mysql_volume.id
  device_name = "/dev/xvdf"
}