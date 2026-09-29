Este proyecto es un **pipeline automatizado de auditoría de rendimiento de campañas de Meta Ads** que combina la manipulación de datos en Python con un modelo de lenguaje local (**Llama 3 en Ollama**). 

Genera un dataset falso pero realista con lógica de negocio publicitaria, realiza el cálculo y agrupamiento determinista de métricas clave con Pandas, y alimenta a un LLM con prompts estructurados para obtener reportes de optimización sin alucinaciones.
El dataset es falso para proteger la privacidad de los datos que serán utilizados, este solo es un ejemplo pequeño de como funciona.

## Tecnologías Utilizadas

* Python 3.12+
* Pandas & NumPy para generar datos falsos y realizar métricas.
* Ollama & Llama 3 para análisis, auditoría y recomendaciones.
* Requests para interactuar con la API REST local de Ollama.
* Tabulate utilizada para el formateo de tablas en Markdown para optimizar el contexto del LLM, ya que el equipo es limitado en este contexto.

---

## Estructura del Proyecto

```text
├── generar_dataset.py        Script para crear el CSV sintético de Meta Ads
├── auditar_meta_ads.py       Script principal (que incluye Pandas + Ollama)
├── meta_ads_fake_dataset.csv  Dataset artificial que generamos
└── README.md                 Documentación del proyecto
