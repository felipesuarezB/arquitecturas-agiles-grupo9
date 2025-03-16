# Experimentos Arquitectura Ágiles de Software 2025-11 Grupo 09

Repositorio de implementación de experimentos del curso.

## Índice

1. [Experimentos](#experimentos)
2. [Estructura](#estructura)
3. [Despliegue](#despliegue)
4. [Autores](#autores)

## Experimentos

Experimento 2: Experimento de mejora de confidencialidad e integridad de microservicio de ventas.

- Componente `api-gateway-service`: Es un servicio que emula un API Gateway como único punto de recepción de peticiones del sistema. Delega generación y validación del Token en `auth-service`.
- Componente `auth-service`: Servicio encargado de verificar la identidad de los usuarios mediante credenciales en texto (usuario y password). 
- Componente `client-service`: Es el servicio que emula las peticiones del cliente y registra los resultados del experimento
- Componente `sales-service`: Es el microservicio que expone operaciones y datos críticos y se protege mediante el `api-gateway-service`.

## Estructura

```txt
  /
    ├── api-gateway-service # Implementación componente monitor.
    ├── auth-service # Implementación componente autenticación y autorización.
    ├── client-service # Implementación componente microservicio de ventas (servicio monitoreado).
    ├── sales-service # Implementación componente microservicio de ventas (servicio monitoreado).
    └── Pipfile # Archivo de declaración de dependencias del proyecto.
```

Experimento 1: Aplicación de tácticas de arquitectura para mejorar la disponibilidad.

- Componente `monitor-service`: Servicio encargado de ejecutar los experimentos y detectar las falllas del servicio `sales-service`. Provee una API para programar experimentos y consultar los resultados.
- Componente `sales-service`: Servicio monitoreado por el servicio `monitor-service`. Encargado de emular fallas de omisión y tiempos de forma aleatoria para el experimento.

## Estructura

```txt
  /
    ├── monitor-service # Implementación componente monitor.
    ├── sales-service # Implementación componente microservicio de ventas (servicio monitoreado).
    └── Pipfile # Archivo de declaración de dependencias del proyecto.
```

## Despliegue

Se despliegan los componentes del experimento en Heroku según la instrucciones de cada README de cada componente.

## Autores

- Danny Zamorano Vallejo - d.zmorano@uniandes.edu.co
- Felipe Suárez - f.suarezb@uniandes.edu.co
- Andy Yair Bolaño Castilla - a.bolanoc@uniandes.edu.co
