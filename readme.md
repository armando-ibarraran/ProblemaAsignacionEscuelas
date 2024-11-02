# Proyecto de Programación para la Planificación Lineal (PPL) - Asignación de Escuelas

Este proyecto contiene la solución a un problema de Programación para la Planificación Lineal (PPL) centrado en la asignación óptima de estudiantes de middle school a diferentes escuelas en la ciudad de Springfield. Este problema surge debido a la decisión de la junta escolar de cerrar una de las escuelas y la necesidad de redistribuir a los estudiantes de manera que minimice los costos de transporte.

El problema puede encontrarse como el **problema 4.3** en el archivo [Case4_2-4_3.pdf](Case4_2-4_3.pdf), donde se detallan las condiciones, restricciones y alternativas a considerar en el proceso de reubicación.

## Descripción del Problema

La junta escolar de Springfield ha decidido cerrar una de sus middle schools, por lo que todos los estudiantes de sexto, séptimo y octavo grado deberán ser reasignados entre las tres escuelas restantes para el próximo año escolar. Como el distrito escolar proporciona transporte a los estudiantes que viven a más de una milla de distancia, la junta busca una asignación que minimice el costo total de transporte.

El costo anual de transporte por estudiante desde cada una de las seis áreas residenciales a cada escuela, junto con datos básicos como la distribución porcentual de estudiantes por grado y otras restricciones, está detallado en la tabla proporcionada en el problema. Las restricciones adicionales incluyen que cada grado debe representar entre el 30% y 36% de la población de cada escuela. El problema permite dividir cada área residencial entre más de una escuela, siempre que los porcentajes de distribución por grado se mantengan constantes.

Como consultor en investigación de operaciones, tu tarea es:
1. **Formular un modelo de programación lineal (PPL)** que resuelva este problema.
2. **Resolver el modelo** para obtener una recomendación de asignación.
3. **Recomendar ajustes** para reducir la división de áreas residenciales entre varias escuelas.
4. **Evaluar alternativas de reducción de costos** eliminando el transporte en distancias específicas.
5. **Ayudar a la junta escolar a tomar una decisión** considerando el costo de transporte y los problemas de seguridad al eliminar opciones de transporte.

## Enfoque Analítico

La versión analítica que fundamenta el código de este proyecto se encuentra en el archivo [NotasAuxiliares.pdf](NotasAuxiliares.pdf), un documento elaborado en equipo. Estas notas incluyen mi versión de la formulación matemática y el análisis de las restricciones y objetivos del problema, proporcionando las bases para la implementación en código.

## Archivos del Proyecto

- **Case4_2-4_3.pdf**: Documento que describe el problema 4.3 y proporciona todos los datos necesarios, restricciones y opciones a evaluar en el problema de asignación de estudiantes.
- **NotasAuxiliares.pdf**: Documento de análisis y formulación matemática del problema. Este documento fue resultado de un esfuerzo colaborativo y sirve como base teórica para la implementación en código.
- **Código fuente**: Archivos de código que implementan la solución del problema de asignación siguiendo el modelo descrito en "NotasAuxiliares.pdf".



