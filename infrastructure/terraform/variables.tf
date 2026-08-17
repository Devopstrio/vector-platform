variable "aws_region" {
  description = "AWS Region"
  default     = "us-east-1"
}

variable "subnet_ids" {
  description = "List of subnet IDs for EKS"
  type        = list(string)
  default     = ["subnet-12345", "subnet-67890"]
}

variable "db_user" {
  description = "Database admin user"
  default     = "postgres_admin"
}

variable "db_password" {
  description = "Database password"
  sensitive   = true
  default     = "super_secure_password"
}
