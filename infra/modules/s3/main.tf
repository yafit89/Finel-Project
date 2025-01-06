resource "aws_s3_bucket" "main" {
  bucket = var.bucket_name

  tags = {
    Name = var.name
  }

resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.aws_s3_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.main.arn
}

output "bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.main.bucket
}