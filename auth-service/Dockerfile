# Imagen Docker base Python.
FROM python:3.12

# Variables de entorno de la aplicación.
# ENV VERSION=
# ENV ENVIRONMENT=
# ENV DB_USER=
# ENV DB_PASSWORD=
# ENV DB_HOST=
# ENV DB_PORT=
# ENV DB_NAME=
# ENV AUTH_SERVICE_URL=
# ENV SALES_SERVICE_URL=
# ENV CLIENT_TIMEOUT=

# Instalar dependencias de la aplicación.
COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system --deploy

# Directorio de instalación.
WORKDIR /app

# Copiar código fuente de la aplicación.
COPY ./src .

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Comando de ejecución aplicación Flask.
# CMD ["flask", "--app", "app", "run", "-h", "0.0.0.0", "-p", "8080"]
CMD flask --app app run -h 0.0.0.0 -p "$PORT"