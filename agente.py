
import os
from Herramientas import resumir_noticia, clasificar_sentimiento, extraer_tickers
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType

# 🔐 Leer API Key
if not os.getenv("OPENAI_API_KEY"):
    with open("api_key.txt") as archivo:
        os.environ["OPENAI_API_KEY"] = archivo.read().strip()

# 🧠 LLM
modelo = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# 🧠 Memoria
memoria = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 🧰 Herramientas
herramientas = [resumir_noticia, clasificar_sentimiento, extraer_tickers]

# 🤖 Agente clásico con memoria
agente = initialize_agent(
    tools=herramientas,
    llm=modelo,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memoria,
    verbose=True
)

# 🔍 Entrada
entrada = input("📰 Ingresa una noticia financiera:\n\n")

# Ejecutar
resultado = agente.invoke({"input": entrada})
respuesta = resultado["output"]

# Separar componentes si el modelo los devuelve mezclados
print("\n📊 Análisis Financiero\n")

if "Resumen:" in respuesta:
    partes = respuesta.split("Resumen:")
    print("📰 Resumen:", partes[1].split("Sentimiento:")[0].strip() if "Sentimiento:" in partes[1] else partes[1].strip())

if "Sentimiento:" in respuesta:
    print("💬 Sentimiento:", respuesta.split("Sentimiento:")[1].split("Ticker")[0].strip())

if "Ticker" in respuesta or "Tickers" in respuesta:
    for palabra in ["Tickers:", "Ticker:"]:
        if palabra in respuesta:
            print("📈 Tickers detectados:", respuesta.split(palabra)[1].strip())
            break