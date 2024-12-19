resource "aws_s3_bucket" "this" {
  bucket = var.yafits3

  versioning {
    enabled = var.s3_versioning
  }

}