from Herramientas import extraer_tickers

texto = """
Las acciones de AAPL y TSLA tuvieron un fuerte movimiento tras el anuncio del nuevo iPhone y la presentación del Cybertruck. Mientras tanto, se espera que AMZN reaccione esta semana.
"""

resultado = extraer_tickers.invoke({"texto": texto})
print("Tickers encontrados:", resultado)