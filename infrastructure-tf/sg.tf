resource "aws_security_group" "kind_cluster_sg" {
  name        = "kind-cluster-sg"
  description = "Security group for Kind Cluster EC2 instance"
  vpc_id      = module.vpc.vpc_id

  # Allow SSH access from any IP
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTP access from any IP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow NodePort access for Flask app
  ingress {
    from_port   = 32371
    to_port     = 32371
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all egress traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "kind-cluster-sg"
    Environment = var.environment
    Project     = var.project_name
  }
}
