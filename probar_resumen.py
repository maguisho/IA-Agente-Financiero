import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Herramientas import resumir_noticia

noticia = """
Apple reportó ingresos récord durante el segundo trimestre gracias al incremento de ventas del iPhone 15 en mercados emergentes como India y Brasil.
"""

resultado = resumir_noticia.invoke({"texto": noticia})
print("📰 Resumen generado:", resultado)