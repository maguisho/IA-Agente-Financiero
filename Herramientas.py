# HERRAMIENTAS.PY
# ────────────────────────────────────────────────
# 🔐 API y MODELO BASE
# ────────────────────────────────────────────────

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.tools import Tool
from pydantic import BaseModel, Field

# Leer clave API desde archivo
with open("api_key.txt") as archivo:
    apikey = archivo.read().strip()
os.environ["OPENAI_API_KEY"] = apikey

modelo = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
parser = StrOutputParser()

# ────────────────────────────────────────────────
# 🔁 SCHEMA DE ENTRADA COMÚN
# ────────────────────────────────────────────────

class EntradaResumen(BaseModel):
    texto: str = Field(description="Texto completo de la noticia financiera")

# ────────────────────────────────────────────────
# 📰 1. HERRAMIENTA: RESUMIR NOTICIA
# ────────────────────────────────────────────────

prompt = ChatPromptTemplate.from_template("Resume la siguiente noticia: {texto}")
cadena_resumen = prompt | modelo | parser

resumir_noticia = cadena_resumen.as_tool(
    name="resumir_noticia",
    description="Resume una noticia financiera para facilitar su análisis",
    args_schema=EntradaResumen
)

# ────────────────────────────────────────────────
# 💬 2. HERRAMIENTA: CLASIFICAR SENTIMIENTO
# ────────────────────────────────────────────────

prompt_sentimiento = ChatPromptTemplate.from_template("""
Analiza el siguiente texto y clasifica el sentimiento general como uno de estos valores:
"Positivo", "Negativo", "Neutral" o "No se puede determinar".

Texto:
{texto}
""")
cadena_sentimiento = prompt_sentimiento | modelo | parser

def ejecutar_sentimiento(texto: str) -> str:
    salida = cadena_sentimiento.invoke({"texto": texto})
    limpio = salida.strip().split("\n")[0].strip().capitalize()
    return limpio

clasificar_sentimiento = Tool(
    name="clasificar_sentimiento",
    description="Determina si el sentimiento del texto financiero es positivo, negativo, neutral o no determinable.",
    func=ejecutar_sentimiento,
    args_schema=EntradaResumen
)

# ────────────────────────────────────────────────
# 📈 3. HERRAMIENTA: EXTRAER TICKERS (INTELIGENTE Y ABIERTA)
# ────────────────────────────────────────────────

from langchain_core.prompts import PromptTemplate

plantilla_tickers = PromptTemplate.from_template("""
A partir del siguiente texto financiero, menciona solo los TICKERS bursátiles (símbolos) de las empresas públicas mencionadas.
Ejemplo de salida: AAPL, TSLA, KO
Si no hay, responde SOLO: NINGUNO.

Texto: {texto}
""")
cadena_tickers = plantilla_tickers | modelo | parser

def detectar_tickers(texto: str) -> list:
    salida = cadena_tickers.invoke({"texto": texto}).strip()
    if "NINGUNO" in salida.upper():
        return []
    return [t.strip() for t in salida.split(",") if t.strip()]

extraer_tickers = Tool(
    name="extraer_tickers",
    description="Extrae los tickers bursátiles (como AAPL, TSLA, KO) mencionados en una noticia financiera.",
    func=detectar_tickers,
    args_schema=EntradaResumen
)

# ────────────────────────────────────────────────
# 💡 4. HERRAMIENTA: RECOMENDACIÓN FINANCIERA
# ────────────────────────────────────────────────

def dar_recomendacion(texto: str) -> str:
    resumen = resumir_noticia.invoke({"texto": texto})
    sentimiento = clasificar_sentimiento.run(texto)
    tickers = extraer_tickers.invoke({"texto": texto})

    if not tickers:
        return "⚠️ No se puede hacer una recomendación porque no se identificaron empresas específicas."

    if sentimiento.lower() == "positivo":
        return f"✅ Recomendación: COMPRAR acciones de {', '.join(tickers)}.\n🟢 Justificación: Sentimiento positivo y contexto favorable."
    elif sentimiento.lower() == "negativo":
        return f"🚫 Recomendación: NO COMPRAR acciones de {', '.join(tickers)}.\n🔴 Justificación: Sentimiento negativo asociado a las empresas."
    elif sentimiento.lower() == "neutral":
        return f"⚖️ Recomendación: OBSERVAR {', '.join(tickers)}.\n🟡 Justificación: Sentimiento neutral, se recomienda precaución."
    else:
        return "❓ No se puede hacer una recomendación clara debido a ambigüedad en el análisis."

recomendador = Tool(
    name="recomendador",
    description="Brinda una recomendación de inversión en base al análisis del texto financiero.",
    func=dar_recomendacion,
    args_schema=EntradaResumen
)