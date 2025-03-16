# Experimentos Arquitectura Ágiles de Software 2025-11 Grupo 09

Repositorio de implementación de experimentos del curso.

## Índice

1. [Experimentos](#experimentos)
2. [Estructura](#estructura)
3. [Despliegue](#despliegue)
4. [Autores](#autores)

## Experimentos

Experimento 2: Aplicación de tácticas para mejorar confidencialidad e integridad en microservicio de ventas.

- Componente `client-service`: Es el servicio que emula las peticiones del cliente y registra los resultados del experimento.
- Componente `api-gateway-service`: Es un servicio que emula un API Gateway como único punto de recepción de peticiones del sistema. Delega generación y validación del Token en `auth-service`.
- Componente `auth-service`: Servicio encargado de verificar la identidad de los usuarios mediante credenciales en texto (usuario y password).
- Componente `sales-service`: Es el microservicio que expone operaciones y datos críticos y se protege mediante el `api-gateway-service`.

Experimento 1: Aplicación de tácticas de arquitectura para mejorar la disponibilidad.

- Componente `monitor-service`: Servicio encargado de ejecutar los experimentos y detectar las falllas del servicio `sales-service`. Provee una API para programar experimentos y consultar los resultados.
- Componente `sales-service`: Servicio monitoreado por el servicio `monitor-service`. Encargado de emular fallas de omisión y tiempos de forma aleatoria para el experimento.

## Estructura

```txt
  /
    ├── api-gateway-service # Implementación API Gateway del sistema.
    ├── auth-service # Implementación componente autenticación y autorización.
    ├── client-service # Implementación componente de ejecución de experimento 2.
    ├── sales-service # Implementación componente microservicio de ventas, servicio monitoreado y protegido por API Gateway.
    ├── monitor-service # Implementación componente monitor y ejecución de experimento 1.
    └── Pipfile # Archivo de declaración de dependencias del proyecto.
```

## Despliegue

Se despliegan los componentes del experimento en ambiente Heroku para experimento 1 y ambiente local para experimento 2 según la instrucciones de cada README de cada componente.

## Autores

- Danny Zamorano Vallejo - d.zmorano@uniandes.edu.co
- Felipe Suárez - f.suarezb@uniandes.edu.co
- Andy Yair Bolaño Castilla - a.bolanoc@uniandes.edu.co
