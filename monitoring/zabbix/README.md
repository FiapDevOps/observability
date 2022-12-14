# Objetivo

![ZABBIX_00](images/ZABBIX_00.png)

Apresentar um cenário com o Zabbix como solução de monitoração centralizada para uma arquitetura simples;

# Caracteriísticas:

Neste laboratório o zabbix será apresentado no seguinte padrão

- Utilizaremos uma infraestrutura centralizada baseada em docker em um modelo all-in-one com mysql, nginx e zabbix rodando em um único container, o modelo pode ser revisado na url: [https://www.zabbix.com/documentation/current/en/manual/installation/containers](https://www.zabbix.com/documentation/current/en/manual/installation/containers) e no repositório [https://github.com/zabbix/zabbix-docker](https://github.com/zabbix/zabbix-docker);
- Criaremos uma configuração explorando templates para monitoração do Sistema Operacional dos servidores com a aplicação docker;

# Instalação do Zabbix

Neste laboratório o ambiente já foi estruturado usando a versão 6 do zabbix em uma instalação baseada em docker compose, para criar o nosso ambiente execute a automação a partir do terraform:

```sh
cd ~/environment/observability/monitoring/zabbix
terraform init
terraform apply 
```

Acesse o Zabbix a partir da url entregue pelo output do terraform:

usuário: Admin
senha: zabbix

Um modelo tradicional de instalação pode ser consultado na documentação oficial do Zabbix:

- [Documentação oficial de instalação do Zabbix](https://www.zabbix.com/download?zabbix=5.4&os_distribution=ubuntu&os_version=20.04_focal&db=postgresql&ws=nginx)
- [Configurando um cenário com autoregistration](https://www.zabbix.com/documentation/2.0/en/manual/discovery/auto_registration)

# Conceitos Básicos

## Hosts
Diferente do modelo de timeseries testado no cenário com o prometheus, no zabbix os endpoits de monitoração são identificados como hosts, o conceito é similar com a diferença prática de que neste formato toda a monitoração é estruturada com base em configurações sobre estes endpoints de fornecimento de dados;

Os hosts são organizados com base em grupos identificados como **Hosts Groups**

## Items
Após a configuração de um host é necessário definir quais as métricas a serem coletadas, essa definição é chamada **Item**, esses items são configurados com base em **Keys** aqui temos um paralelo direto ao timeseries, uma Key é essencialmente uma expressão lógica com uma informação a ser coletada, como consumo de CPU ou uso total de disco, por exemplo;

## Triggers
As triggers também são identificadas como problem expression e basicamente seguem o mesmo conceito em qualquer plataforma de monitoração, elas definem qual a consulta e resposta (trigger expression) que identificam um problema e sua respectiva severidade;

## Actions
As Actions são efetivamente o processo de alerta e de tarefas executadas a partir do disparado de triggers com base em condições e operações ou ações que devem ser executadas, uma action pode ser usada para alertar um plantonista com base no envio de e-mail ou Post em uma plataforma como o Telegram ou Slack.

---

##### Fiap - MBA DEVOPS Engineering
profhelder.pereira@fiap.com.br

**Free Software, Hell Yeah!**
