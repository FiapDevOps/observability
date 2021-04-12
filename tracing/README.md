# Tracing
Deploy a python app usando instrumentação baseada em opentelemetry para apresentar o conceito de tracing

![alt tag](https://github.com/FiapDevOps/observability/blob/f51fda6fcb4ad00777dd3012d6505c1c0800c6db/img-src/jeager_logo.png)


Neste laboratório executaremos testes básicos de análise do processo de configuração de trace de aplicações usando um modelo python/flask e as bibliotecas do projeto opentelemetry;

* A versão original da aplicação é um projeto python usando flask preparado para construção em container, um modelo de construção similar pode ser obtido para estudo no portal Real Python: [https://realpython.com/flask-by-example-part-1-project-setup/](https://realpython.com/flask-by-example-part-1-project-setup/);


* Para configurar o processo de rastreio de etapas da execução da aplicação flask configuramos a biblioteca [opentelemetry-python](https://opentelemetry-python.readthedocs.io/en/latest/getting-started.html);

* Algumas etapas do processo de configuração foram divididas em exemplos menores para execução direta;

## Exemplo 1: Testando o opentelemetry em Python

O exemplo abaixo foi obtido a partir da [Documentação](https://opentelemetry-python.readthedocs.io/) do projeto opentelemetry-python, basicamente, este é o processo mínimo necessário para configurar a emissão de spans a partir de uma aplicação, neste caso com exibição em STDOUT:

```sh
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("test_span_01"):
    with tracer.start_as_current_span("test_span_02"):
            print("SRE and DevOps work together!!!")
```

1.1 Para a execução faça a instalação das dependências da App que será configurada a seguir e em seguida faça uma chamada direta ao arquuivo **'example_tracing.py'** utilizando um interpretador de comandos Python:

```sh
pip3 install opentelemetry-api
pip3 install opentelemetry-sdk

python3 example_tracing.py
```

> No resultado você obterá o primeiro OUTPUT de processo de rastreio, um tracing estruturado em duas operações consecutivas, conceitualmente cada operação refere-se a uma etapa de execução de funções e/ou chamadas dentro da aplicação.

## Exemplo 2: Exportando dados para observability:

Um span como o modelo usado no exemplo anterior terá uma relação detalhada de dados de instrumentação, em um contexto prático para que esses dados se transformem em informações reçevantes para observability será necessário exportar esses spans para um backend de monitoração.

2.1 Nesta etapa será necessário um componente dentro da infraestrutura que seja capaz de injerir e disponibilizar os dados de tracing, neste laboratório uma versão simplificada do [projeto jeager](https://www.jaegertracing.io/) será utilizada:

2.2 Execute a aplicação abaixo para criar o backend do jaeger (trata-se de uma versão centralizada com as funções de banco de dados e consumidor dos registros de tracing além da UI de exibição):

```sh
docker run --rm --name jeager -d \
    -p 8080:16686 \
    -p 6831:6831/udp \
    jaegertracing/all-in-one
```

2.3 Nesta execução escolhi publicar a app na porta 8080 (A interface de acesso será aberta nesta porta), já porta 6831/udp ficará responsável pela injestão dos dados enviados pela app do exemplo abaixo:

```sh
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "example_exporter"})
    )
)

# https://opentelemetry-python.readthedocs.io/en/latest/exporter/jaeger/jaeger.html

# create a JaegerExporter
jaeger_exporter = JaegerExporter(
    # configure agent
    agent_host_name='localhost',
    agent_port=6831,
    # optional: configure also collector
    # collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
    # username=xxxx, # optional
    # password=xxxx, # optional
    # max_tag_value_length=None # optional
)

# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(jaeger_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("test_span_01"):
    with tracer.start_as_current_span("test_span_02"):
            print("SRE and DevOps work together!!!")
```

2.4 Execute a instalação do exporter e em seguia a aplicação **'example_exporter'**, dessa vez o modelo de envio dos spans substituiu a exibição em STDOUT pelo disparado dos dados para o jeager usando o exporter [opentelemetry.exporter.jaeger](https://opentelemetry-python.readthedocs.io/en/latest/exporter/jaeger/jaeger.html):

```sh
pip3 install opentelemetry.exporter.jaeger
python3 example_exporter.py
```

2.5 Você verá uma interface similar ao modelo abaixo, para o processo de filtro utilize o nome do serviço estruturado na aplicação como **'example_exporter'**;

![alt tag](https://github.com/FiapDevOps/observability/blob/f51fda6fcb4ad00777dd3012d6505c1c0800c6db/img-src/jeager_01.png)


## Exemplo 3: Incorporando o tracing a nossa App em Flask

De forma similar a aobrdagem utilizada no laboratório de monitoração, neste exemplo a mesma aplicação base das aulas anteriores foi configurada  com envio de tracing ao Jeager usando instrumentação.

> No OpenTelemetry o conceito de instrumentação refere-se a pacotes projetados para fazer interface com uma estrutura ou biblioteca específica, como Flask em nosso caso;

3.1 Para essa construção basicamente adicionaremos as bibliotecas de instrumentação a relação de requeriments ou com instalação direta via pip:

```sh
pip3 install opentelemetry-instrumentation-flask
```

* Verifique o códido base para essa construção no arquivo **'example_instrumentation.py'**

* O modelo completo do exemplo no diretório app onde uma versão com instrumentação dos dados de tracing para envio ao jegaer e configuração de exibição em STDOUT para acompanhamento no lab foi estruturada;


3.2 A partir do diretório deste do documento em observability/tracing execute:

```sh
docker build app -t sample
docker run --net host -d --rm --name sample -e PORT=80 sample
docker ps
```

Nesta etapa dosi containers foram criados:

| nome | descrição                       | porta                             |
|------|---------------------------------|-----------------------------------|
| sample | Entrega da app com instrumentação usando opentelemetry           | \<IP-APP>:80                      |
| jeager | Stack Jeager com acesso a UI            | \<IP-APP>:8080                    |

Faça um teste acessando a aplicação na porta 80, ao executar o acesso o span será disparado em STDOUT e ao mesmo tempo enviado ao jeager;

---
##### Fiap - MBA DevOps Enginnering | SRE
profhelder.pereira@fiap.com.br

**Free Software, Hell Yeah!**
