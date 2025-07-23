# analisis_financiero.py
import os
from Herramientas import resumir_noticia, clasificar_sentimiento, extraer_tickers, dar_recomendacion
from newspaper import Article
import validators

# Leer API key desde archivo txt
if not os.getenv("OPENAI_API_KEY"):
    with open("api_key.txt") as archivo:
        os.environ["OPENAI_API_KEY"] = archivo.read().strip()

# Ingreso de texto o URL
entrada = input("📰 Ingresa una noticia financiera (texto o URL):\n\n")

if validators.url(entrada):
    print("🔎 Cargando contenido desde la URL...")
    try:
        articulo = Article(entrada)
        articulo.download()
        articulo.parse()
        texto = articulo.text
    except Exception as e:
        print("⚠️ No se pudo extraer el texto de la URL. Error:", e)
        texto = ""
else:
    texto = entrada

# Validación mínima
if not texto.strip():
    print("⚠️ No se proporcionó texto válido para analizar.")
    exit()

# Ejecutar herramientas
resumen = resumir_noticia.invoke({"texto": texto})
sentimiento = clasificar_sentimiento.run(texto)
tickers = extraer_tickers.invoke({"texto": texto})
recomendacion = dar_recomendacion(texto)

# Formatear salida
print("\n📊 Análisis Financiero\n")
print("📰 Resumen:", resumen)
print("💬 Sentimiento:", sentimiento)
print("📈 Tickers detectados:", ", ".join(tickers) if tickers else "NINGUNO")
print("\n💡 Recomendación:\n" + recomendacion)

