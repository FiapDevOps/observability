# https://www.terraform.io/language/values/outputs

output "prometheus_public_ip" {
  value = aws_instance.elk_stack.public_ip
  description = "The ELK stack public ip address"
}

output "prometheus_private_ip" {
  value = aws_instance.elk_stack.private_ip
  description = "The ELK stack private ip address"
}
