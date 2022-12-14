# https://www.terraform.io/language/values/outputs

output "zabbix_private_ip" {
  value = aws_instance.zabbix.private_ip
  description = "The zabbix private ip address"
}

output "zabbix_public_ip" {
  value = aws_instance.zabbix.public_ip
  description = "The zabbix public ip address"
}

output "zabbix_private_dns" {
  value = aws_instance.zabbix.private_dns
  description = "The zabbix private dns address"
}

output "zabbix_public_dns" {
  value = aws_instance.zabbix.public_dns
  description = "The zabbix public FQDN"
}

output "app_private_ip" {
  value = aws_instance.app[0].private_ip
  description = "The mediawiki private ip address"
}

output "app_private_dns" {
  value = aws_instance.app[0].private_dns
  description = "The mediawiki private dns address"
}

output "app_public_ip" {
  value = aws_instance.app[0].public_ip
  description = "The mediawiki public ip address"
}

output "app_public_dns" {
  value = aws_instance.app[0].public_dns
  description = "The mediawiki app public FQDN"
}