# Monitoring [Parte 1]
Deploy a python app usando prometheus como ferramenta de monitoração

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
docker run --rm --name little-app -d -e PORT=8080 -p 8080:8080 little-app:0.1
```

1.3 Após o processo de build você verá um exemplo da aplicação rodando no endereço 127.0.0.1:8080:

| descrição                       | path                              |
|---------------------------------|-----------------------------------|
| Entrega da aplicação            | \<IP-APP>:8080                     |
| Scrape de métricas              | \<IP-APP>:8080/metrics             |

```sh
curl 127.0.0.1
curl 127.0.0.1/metrics
```

1.4 A aplicação anterior utilziada no teste será iniciada novamente dentro da arquitetura de rede onde está configurado o prometheus e os outros componentes do laboratório, para isso para a aplicação anterior:

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
| Entrega da aplicação Pytho           | <IP-APP>:8080                     |
| Entrega da monitoração time series   | <IP-APP>:9090                     |


1.6. Em nosso modelo temos 3 targets configurados para expor métricas via timeseries, cada um deles é identificado por um job da configuração e podem ser consultados na instância onde rodamos nosso stack na path ":9090/targets";

---
##### Fiap - MBA DevOps Enginnering | SRE
profhelder.pereira@fiap.com.br

**Free Software, Hell Yeah!**