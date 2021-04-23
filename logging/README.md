# Logging

Este laboratório é uma reprodução do exemplo citado no artigo apresentado no portal logz.io, [Disponível neste endereço](https://logz.io/blog/elk-stack-on-docker/);

## Alterações:

Na prática a única mudança relevante refere-se a implantação do filebeat com scrape de logs direto dos containers, como consequeência neste exemplo é necessário que os containers tenham interação com o sistema operacional, a stack foi baseada em uma arquitetura de Docker Enterprise rodando em Linux;

Em um segundo ponto de custmização adicionei um exemplo com um log estruturado em formato Json, como prova conceito para a pardonização de logs em estruturas de indexação e como essa escolha facilitaria processos de busca e identificação de padrões para observability, essa mudança foi aplicada diretamente no nginx com alterações no template do arquivo [nginx.conf](https://raw.githubusercontent.com/fiapdevops/observability/main/logging/nginx/config/nginx.conf);

---
##### Fiap - MBA DevOps Enginnering | SRE
profhelder.pereira@fiap.com.br

**Free Software, Hell Yeah!**