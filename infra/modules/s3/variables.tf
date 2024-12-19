variable "bucket_name" {
  description = "The name of the S3 bucket."
  type        = string
}

variable "versioning" {
  description = "Enable versioning for the S3 bucket."
  type        = bool
  default     = true
}