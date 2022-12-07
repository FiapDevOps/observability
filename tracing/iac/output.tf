# https://www.terraform.io/language/values/outputs

output "jeager_public_ip" {
  value = aws_instance.tracing_app.public_ip
  description = "The demo app with jeager public ip address"
}

output "jeager_private_ip" {
  value = aws_instance.tracing_app.private_ip
  description = "The demo app with jeager private ip address"
}