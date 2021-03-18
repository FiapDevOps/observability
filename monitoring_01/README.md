# Monitoring [Parte 1]
Deploy a python app usando prometheus como ferramenta de monitoração

![alt tag](https://raw.githubusercontent.com/FiapDevOps/observability/f8ccc0419face4b2b99aea68536d21551c699bc7/img-src/prometheus_logo.png)


Para testar a aplicação verifique o conteúdo do diretório build em relação aos seguintes pontos:

1.1 A versão original da aplicação é um projeto python usando flask preparado para construção em container, um modelo de construção similar pode ser obtido para estudo no portal Real Python: [https://realpython.com/flask-by-example-part-1-project-setup/](https://realpython.com/flask-by-example-part-1-project-setup/);


1.2. Nesta versão da aplicação foi adicionada uma biblioteca para construção das métricas no prometheus, o [prometheus-flask-exporter](https://pypi.org/project/prometheus-flask-exporter/), acessível a partir do endpoit /metrics;

1.3 Além disso também adicionamos um Dockerfile, pois o modelo descrito nesse Lab utiliza DockerCompose para entregar todos os serviços necessários usando uma camada de abstração de rede e evitando conflitos de endereço IP:

```sh
FROM python:3.8-alpine

# Padronizacao do Workdir
WORKDIR /src

# Instalacao de Dep.
COPY requeriments.txt .
RUN pip install -r requeriments.txt
COPY src/ .

# Execução da app
CMD [ "python", "./app.py" ]
```

1.4 Para gerar o artefato que será utilizado no laboratório acesse o diretório do projeto e execute o build do container:

```sh
cd $HOME/observability/monitoring_01/app/
docker build . -t little-app:0.1
docker run --rm --name little-app -d -e PORT=8080 -p 80:8080 little-app:0.1
```

1.3 Após o processo de build você verá um exemplo da aplicação rodando no endereço 127.0.0.1:8080:

| descrição                       | path                              |
|---------------------------------|-----------------------------------|
| Entrega da aplicação            | \<IP-APP>:80                     |
| Scrape de métricas              | \<IP-APP>:80/metrics             |

```sh
curl 127.0.0.1
curl 127.0.0.1/metrics
```

1.4 A aplicação anterior utilizada no teste será iniciada novamente na arquitetura de rede onde está configurado o prometheus e os outros componentes do laboratório, para isso para a aplicação anterior:

```sh
docker kill little-app
docker ps
```

1.5. Inicie o conjunto de containers que fazem a composição do laboratório com Docker compose:

```sh
cd $HOME/observability/monitoring_01/
docker-compose up -d
```

Se o processo de build ocorrer conforme esperado e as imagens do prometheus e do segundo componente que trataremos no futuro forem baixadas teremos o seguinte cenário:

| descrição                            | path                              |
|--------------------------------------|-----------------------------------|
| Entrega da aplicação Python          | <IP-APP>:80                       |
| Entrega da monitoração time series   | <IP-APP>:9090                     |
| Entrega da monitoração da instância  | 127.0.0.1:9100                    |


1.6. Em nosso modelo temos 4 targets configurados para expor métricas via timeseries, cada um deles é identificado por um job da configuração e podem ser consultados na instância onde rodamos nosso stack na path ":9090/targets";

---

# Consultando Indicadores

No modelo entregue temos uma aplicação web, respondendo a requisições HTTP e exportando métricas, dados que serão usados para produzir alguns exemplo de SLI:

2.1 Considere uma métrica simples filtrando requisições http com base no status code:

```sh
flask_http_request_total{status=~"2.."}
```

2.2 Poderiamos interpretar que requisições com status code diferente de 200 representam o indicador desejado (o que provavelmente não é verdade):

```sh
sum(rate(flask_http_request_total{status=!"2.."}[5m]))
```

2.3 Melhorando a estratégia poderiamos filtrar apenas requisições com status code 500, o que provavelmente se aproximaria mais de um cenário onde a falha relativa ao serviço é vinculada a comportamento inesperado em um backend.

```sh
sum(rate(flask_http_request_total{status=~"5.."}[5m]))
```

# Gerando um SLO

SLO são sempre baseados em um período de tempo, para o teste anterior a função rate foi utilizada para calcular a quantidade de requisições com retorno 5xx em um intervalo de 5 minutos, utilizando a equação básica para um calculo de disponibilidade poderiamos construir o seguinte cenário:

```sh
sum(rate(flask_http_request_total{job="app", status!~"5.."}[10m])) /  
sum(rate(flask_http_request_total{job="app"}[10m])) * 100
```

> Dentro dos últimos 10 minutos estamos analisando qual a taxa de eventos executados com sucesso (códig ode status diferente de 5xx), ou seja: Eventos válidos dívido pelo total de eventos ocorridos;

---
##### Fiap - MBA DevOps Enginnering | SRE
profhelder.pereira@fiap.com.br

**Free Software, Hell Yeah!**
