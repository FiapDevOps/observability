# Tracing
Deploy a python app usando instrumentação baseada em opentelemetry para apresentar o conceito de tracing

![alt tag](https://github.com/fiapdevops/observability/blob/f51fda6fcb4ad00777dd3012d6505c1c0800c6db/img-src/jeager_logo.png)


Neste laboratório executaremos testes básicos de análise do processo de configuração de trace de aplicações usando um modelo python/flask e as bibliotecas do projeto opentelemetry;

* A versão original da aplicação é um projeto python usando flask preparado para construção em container, um modelo de construção similar pode ser obtido para estudo no portal Real Python: [https://realpython.com/flask-by-example-part-1-project-setup/](https://realpython.com/flask-by-example-part-1-project-setup/);


* Para configurar o processo de rastreio de etapas da execução da aplicação flask configuramos a biblioteca [opentelemetry-python](https://opentelemetry-python.readthedocs.io/en/latest/getting-started.html);

* Algumas etapas do processo de configuração foram divididas em exemplos menores para execução direta;

Para este laboratório será necessárioa a instalação de algumas bibliotecas, utilizaremos um container em Docker para padronizar a configuração e testes e uma rede dentro do docker para a comunicação entre a app e o jaeger responsável por receber os dados de telemetria:

Crie a rede interna para comunicação entre os containers:
```sh
docker network create lab
docker network ls
```

A partir da raiz do repositório clonado execute:
```sh
docker run -it --rm --name app --network lab -v $PWD/exemplos:/app python:3.8 bash
```

Você será direcionado a um terminal dentro do container:

```sh
# O diretório "/app" contém os modelos que executaremos antes de rodar a stack completa com jeager
cd /app
ls

# Instale as dependências necessárias para os três exemplos seguintes:
pip install -r requeriments.txt
```

## Exemplo 1: Testando o opentelemetry em Python

O exemplo abaixo foi obtido a partir da [Documentação](https://opentelemetry-python.readthedocs.io/) do projeto opentelemetry-python, basicamente, este é o processo mínimo necessário para configurar a emissão de spans configurando a telemetria dentro da aplicação, neste caso com exibição em STDOUT:

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
pip install opentelemetry-api opentelemetry-sdk
python example_tracing.py
```

> No resultado você obterá o primeiro OUTPUT de processo de rastreio, um tracing estruturado em duas operações consecutivas, conceitualmente cada operação refere-se a uma etapa de execução de funções e/ou chamadas dentro da aplicação, o que na prática significa que a abertura de span provavelmente ocorrerá em etapas distintas dentro do código, como no inicío de uma função de roteamento de requisições e em seguida no início do processo de escrita em um banco de dados.

## Exemplo 2: Exportando dados para observability:

Um span como o modelo usado no exemplo anterior terá uma relação detalhada de dados de instrumentação, em um contexto prático para que esses dados se transformem em informações relevantes para observability será necessário exportar esses spans para um backend de monitoração.

2.1 Nesta etapa será necessário um componente dentro da infraestrutura que seja capaz de injerir e disponibilizar os dados de tracing, neste laboratório uma versão simplificada do [projeto jeager](https://www.jaegertracing.io/) será utilizada:

2.2 Em um segundo terminal execute a aplicação abaixo para criar o backend do jaeger (trata-se de uma versão centralizada com as funções de banco de dados e consumidor dos registros de tracing além da UI de exibição):

```sh
docker run --rm --name jaeger -d \
    -p 8080:16686 \
    -p 6831:6831/udp \
    --network lab \
    jaegertracing/all-in-one
```

2.3 Nesta execução escolhi publicar o exporter na porta 8080 (A interface de acesso será aberta nesta porta), já porta 6831/udp ficará responsável pela injestão dos dados enviados pela app do exemplo abaixo:

```sh
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({
            "service.name": "example_exporter"
        }),
    ),
)

# Configurando o agente do jeager
# From https://opentelemetry-python.readthedocs.io/en/latest/exporter/jaeger/jaeger.html
jaeger_exporter = JaegerExporter(
    agent_host_name='localhost',
    agent_port=6831,
)

# Criando um span e vinculando a um BatchSpanProcessor para envio ao Jeager
# https://opentelemetry-python.readthedocs.io/en/stable/sdk/trace.export.html?highlight=BatchSpanProcessor#opentelemetry.sdk.trace.export.BatchSpanProcessor
span_processor = BatchSpanProcessor(jaeger_exporter)

# Neste exemplo adicionamos o dados de telemetria ao tracer a partir do batch declarado acima:
trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("test_span_01"):
    with tracer.start_as_current_span("test_span_02"):
            print("SRE and DevOps work together!!!")
```

2.4 Execute a instalação do exporter e em seguia a aplicação **'example_exporter'**, dessa vez o modelo de envio dos spans substituiu a exibição em STDOUT pelo disparado dos dados para o jeager usando o exporter [opentelemetry.exporter.jaeger](https://opentelemetry-python.readthedocs.io/en/latest/exporter/jaeger/jaeger.html):

```sh
pip install opentelemetry.exporter.jaeger
python example_exporter.py
```

2.5 Acessando a porta publicada anteriormente você verá uma interface similar ao modelo abaixo, para o processo de filtro utilize o nome do serviço estruturado na aplicação como **'example_exporter'**;

![alt tag](https://github.com/FiapDevOps/observability/blob/f51fda6fcb4ad00777dd3012d6505c1c0800c6db/img-src/jeager_01.png)

2.6 Destrua o lab anterior removendo os containers e a docker network:

```sh
docker kill app jaeger
docker network rm lab
```

## Exemplo 3: Incorporando o tracing a nossa App em Flask

De forma similar a abordagem utilizada no laboratório de monitoração, neste exemplo a mesma aplicação base das aulas anteriores foi configurada  com envio de tracing ao jaeger usando instrumentação.

```sh
import os
import signal
from flask import Flask

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor


trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({
            "service.name": "service_example"
        }),
    ),
)

# Configurando o agente do jeager
# From https://opentelemetry-python.readthedocs.io/en/latest/exporter/jaeger/jaeger.html
jaeger_exporter = JaegerExporter(
    agent_host_name='jaeger',
    agent_port=6831,
)

# Criando um span e vinculando a um BatchSpanProcessor para envio ao Jeager
# https://opentelemetry-python.readthedocs.io/en/stable/sdk/trace.export.html?highlight=BatchSpanProcessor#opentelemetry.sdk.trace.export.BatchSpanProcessor
span_processor = BatchSpanProcessor(jaeger_exporter)

# Neste exemplo adicionamos o dados de telemetria ao tracer a partir do batch declarado acima:
trace.get_tracer_provider().add_span_processor(span_processor)

# Finalmente invocamos novamente a aplicação e iniciamos um processo de tracer dentro da função hello:
# O FlaskInstrumentor servirá para instrumentar os dados do Framework flask com os detalhes da requisição HTTP:
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def hello():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span('test_span'):
        return "SRE and DevOps work together!!! "

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
```

Este exemplo será executado utilizando um container compilando uma versão da app com a amostra de tracing:

3.1. Inicie o terraform:

```sh
cd observability/tracing/iac
terraform init
terraform plan
```

3.2. Verifique a partir do plan que o modelo fara a entrega de uma instancia ubuntu com base no template de [cloud-init](https://cloudinit.readthedocs.io/en/latest/) alocado no diretório "iac/templates" bem como as regras de liberação dos grupos de segurança da app

```sh
terraform apply
```

---

Nesta etapa dois containers foram criados:

| nome | descrição                       | porta                             |
|------|---------------------------------|-----------------------------------|
| sample | Entrega da app com instrumentação usando opentelemetry           | \<IP-APP>:80                      |
| jeager | Stack Jeager com acesso a UI            | \<IP-APP>:8080                    |

Faça um teste acessando a aplicação na porta 80, ao executar o acesso o span será disparado em STDOUT e ao mesmo tempo enviado ao jeager;

---

##### Fiap - MBA
profhelder.pereira@fiap.com.br

**Free Software, Hell Yeah!**