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
