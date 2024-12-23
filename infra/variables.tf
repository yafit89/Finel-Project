variable "default_ports" {
  description = "List of default ports to open in the security group"
  type        = list(number)
  default     = [80, 443]
}

variable "extra_ports" {
  description = "Additional ports to open in the security group"
  type        = list(number)
  default     = [22, 3306]
}

variable "environment" {
  description = "Environment tag (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_id" {
  description = "Work VPC IP"
  type        = string
  default     = "vpc-0299060595460e45b"
}
