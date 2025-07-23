from Herramientas import clasificar_sentimiento

texto = "Ayer se dieron declaraciones variadas sobre el desempeño económico, con opiniones divididas."
resultado = clasificar_sentimiento.invoke({"texto": texto})
print("🔍 Sentimiento:", resultado)