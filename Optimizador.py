import json
import pandas as pd
import requests

# Cargamos el dataset
df = pd.read_csv("meta_ads_fake_dataset.csv")

# Se agrupa por campaña y plataforma como en el dataset falso
resumen = (
    df.groupby(["campaign_name", "publisher_platform"])
    .agg(
        {
            "spend": "sum",
            "impressions": "sum",
            "clicks": "sum",
            "conversions": "sum",
            "conversion_value": "sum",
        }
    )
    .reset_index()
)

# se calculan metricas estrictas para asegurar la precisión de la respuesta
resumen["ctr_%"] = (resumen["clicks"] / resumen["impressions"] * 100).round(2)
resumen["cpc_$"] = (resumen["spend"] / resumen["clicks"]).round(2)
resumen["cpa_$"] = (
    (resumen["spend"] / resumen["conversions"]).fillna(0).round(2)
)
resumen["roas"] = (resumen["conversion_value"] / resumen["spend"]).round(2)

# convertimos la tabla para no saturar a Ollama
tabla_resumen_string = resumen.to_markdown(index=False)

# 4. prompts específicos para evitar alucinaciones de Ollama
prompt_sistema = (
    "Eres un director de marketing digital y growth hacker implacable. "
    "REGLA OBLIGATORIA: Basándote ÚNICAMENTE en la tabla proporcionada, audita el rendimiento. "
    "NO inventes métricas inexistentes (como demografía, CPV o edad). Sé duro, directo y preciso con los números reales."
)

prompt_usuario = f"""Aquí tienes el reporte consolidado de rendimiento de Meta Ads:

{tabla_resumen_string}

Por favor, analiza estos datos y responde:
1. ¿Qué campañas y plataformas están quemando dinero? (Menciona sus nombres, gasto real, CPA o ROAS exacto de la tabla).
2. ¿Qué fallos de rendimiento observas en el CTR, CPC o ROAS de estas campañas?
3. Tres recomendaciones concretas y accionables para reasignar el presupuesto hacia las opciones más rentables.
"""

# se lo pedimos a Ollama finalmente
url = "http://localhost:11434/api/generate"

payload = {
    "model": "llama3",
    "prompt": f"{prompt_sistema}\n\n{prompt_usuario}",
    "stream": False,
}

print("Agrupando datos y enviando reporte resumido a Ollama...")
response = requests.post(url, json=payload)

if response.status_code == 200:
    resultado = response.json().get("response", "no se obtuvo respuesta")
    print("\n--- REPORTE DE AUDITORÍA REAL ---\n")
    print(resultado)
else:
    print(f"Error al conectar con Ollama: {response.status_code}")