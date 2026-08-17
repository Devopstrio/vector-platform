provider "aws" {
  region = var.aws_region
}

# Simulate EKS Cluster Provisioning
resource "aws_eks_cluster" "vector_cluster" {
  name     = "devopstrio-vector-platform"
  role_arn = aws_iam_role.eks_role.arn

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

# Simulate RDS PostgreSQL for Metadata
resource "aws_db_instance" "metadata_db" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.micro"
  db_name              = "vector_metadata"
  username             = var.db_user
  password             = var.db_password
  skip_final_snapshot  = true
}

# Simulate IAM Role
resource "aws_iam_role" "eks_role" {
  name = "eks-cluster-role"
  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}
