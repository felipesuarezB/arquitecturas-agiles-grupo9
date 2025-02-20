# Experimentos Arquitectura Ágiles de Software 2025-11 Grupo 09

Repositorio de implementación de experimentos del curso.

## Índice

1. [Experimentos](#experimentos)
2. [Estructura](#estructura)
3. [Despliegue](#despliegue)
4. [Autores](#autores)

## Experimentos

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
