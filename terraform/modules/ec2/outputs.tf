output "public_ip" {
  description = "Elastic (static) public IP address"
  value       = aws_eip.app.public_ip
}

output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.app.id
}
