# Experimento 1 Arquitectura Ágiles de Software 2025-11 Grupo 09

Experimentos 1 de aplicación de tácticas de arquitectura para mejorar la disponibilidad.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Autores](#autores)

## Estructura

```txt
monitor-service/
    ├── src/ # Código de la aplicación backend.
    ├── Dockerfile # Archivo para la creación de imagen Docker.
    └── Pipfile # Archivo de declaración de dependencias del proyecto.
```

## Ejecución

Primero, instale las dependencias del proyecto:

```bash
  pipenv install
```

Luego, ejecute el proyecto en modo local para pruebas:

```bash
  pipenv run flask -e .env.test --app src/app run -h 0.0.0.0 -p 8080 --debug
```

O ejecute el proyecto en modo productivo:

```bash
  pipenv run flask --app src/app run -h 0.0.0.0 -p 8080
```

Para ejecutarlo como Docker container, primero se debe construir la imagen con el siguiente comando:

```bash
  docker build -t monitor-service:1.0 .
```

Luego se puede arrancar un container en modo test con el siguiente comando:

```bash
  docker run -d -p 8080:8080 -e PORT=8080 -e ENVIRONMENT=test -e DB_HOST=memory monitor-service:1.0
```

## Uso

Para consumir la API siga la definición de los endpoints en la ruta `/swagger-ui`. Para descargar la definición de las APIs en formato OpenAPI abra la ruta `/api-spec.json`.

## Despliegue

Para el despliegue en Heroku se deben ejecutar los siguientes comandos:

```bash
  heroku login
  heroku container:login
  heroku stack:set container --app <heorku-app-name>

  heroku container:push web --app <heorku-app-name>
  heroku container:release web --app <heorku-app-name>
```

Para leer logs en Heroku ejecutar el siguiente comando:

```bash
  heroku logs --app <heorku-app-name> --tail
```

Para reiniciar la app en Heroku ejecutar el siguiente comando:

```bash
  heroku restart --app <heorku-app-name>
```

## Autores

- Danny Zamorano Vallejo - d.zmorano@uniandes.edu.co
- Felipe Suárez - f.suarezb@uniandes.edu.co
- Andy Yair Bolaño Castilla - a.bolanoc@uniandes.edu.co
