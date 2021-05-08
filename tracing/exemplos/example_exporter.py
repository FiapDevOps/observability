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
    agent_host_name='jaeger',
    agent_port=6831,
)

# Criando um span e vinculando a um BatchSpanProcessor para envio ao Jeager
# https://opentelemetry-python.readthedocs.io/en/stable/sdk/trace.export.html?highlight=BatchSpanProcessor#opentelemetry.sdk.trace.export.BatchSpanProcessor
span_processor = BatchSpanProcessor(jaeger_exporter)

# Neste exemplo adicionamos o dados de telemetria ao tracer a partir do batch declarado acima:
trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("teste_com_span"):
            print("SRE and DevOps work together!!!")
