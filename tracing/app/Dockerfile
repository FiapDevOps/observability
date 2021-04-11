FROM python:3.8

# Padronizacao do Workdir
WORKDIR /src

# Instalacao de Dep.
COPY requeriments.txt .
RUN pip install -r requeriments.txt
COPY src/ .

# Execução da app
CMD [ "python", "./example_app_instrumentation.py" ]