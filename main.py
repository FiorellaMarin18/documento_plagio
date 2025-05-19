import tkinter as tk
from tkinter import filedialog, messagebox
import re
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download("punkt")
nltk.download("stopwords")

# Función para extraer texto de PDF
def extraer_texto_pdf(ruta):
    with open(ruta, 'rb') as f:
        lector = PdfReader(f)
        texto = ''
        for pagina in lector.pages:
            texto += pagina.extract_text()
    return texto

# Función para limpiar texto
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'\d+', '', texto)
    texto = re.sub(r'[^\w\s]', '', texto)
    tokens = word_tokenize(texto, language='spanish')
    palabras_filtradas = [p for p in tokens if p not in stopwords.words('spanish') and len(p) > 2]
    return palabras_filtradas

# Riqueza léxica
def calcular_riqueza_lexica(palabras):
    if len(palabras) == 0:
        return 0
    return len(set(palabras)) / len(palabras)

# Similaridad usando trigramas
def calcular_similitud(p1, p2):
    set1 = set(zip(p1, p1[1:], p1[2:]))
    set2 = set(zip(p2, p2[1:], p2[2:]))
    if not set1 or not set2:
        return 0
    return 100 * len(set1 & set2) / len(set1 | set2)

# Graficar palabras más comunes
def graficar_palabras_comunes(p1, p2):
    total = p1 + p2
    frecuencias = {}
    for palabra in total:
        frecuencias[palabra] = frecuencias.get(palabra, 0) + 1
    comunes = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)[:10]
    palabras, valores = zip(*comunes)
    plt.figure(figsize=(8, 5))
    plt.bar(palabras, valores, color='skyblue', edgecolor='black')
    plt.title("Palabras más comunes en ambos textos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("grafica_comparacion.png")
    plt.show()

# Función principal
def analizar_textos():
    archivo1 = filedialog.askopenfilename(title="Seleccionar primer PDF", filetypes=[("PDF files", "*.pdf")])
    archivo2 = filedialog.askopenfilename(title="Seleccionar segundo PDF", filetypes=[("PDF files", "*.pdf")])
    
    if not archivo1 or not archivo2:
        messagebox.showerror("Error", "Debes seleccionar dos archivos PDF.")
        return
    
    texto1 = extraer_texto_pdf(archivo1)
    texto2 = extraer_texto_pdf(archivo2)
    
    palabras1 = limpiar_texto(texto1)
    palabras2 = limpiar_texto(texto2)
    
    riqueza1 = calcular_riqueza_lexica(palabras1)
    riqueza2 = calcular_riqueza_lexica(palabras2)
    similitud = calcular_similitud(palabras1, palabras2)

    resultado = (
        f"Riqueza léxica del Documento 1: {riqueza1:.2f}\n"
        f"Riqueza léxica del Documento 2: {riqueza2:.2f}\n"
        f"Probabilidad de similitud (posible plagio): {similitud:.2f}%"
    )

    # Guardar resultados en .txt
    with open("resultado_analisis.txt", "w", encoding="utf-8") as f:
        f.write("RESULTADO DEL ANÁLISIS\n")
        f.write("======================\n")
        f.write(resultado + "\n")
        f.write("Gráfica guardada como: grafica_comparacion.png\n")

    messagebox.showinfo("Resultado", resultado)

    # Mostrar gráfica
    graficar_palabras_comunes(palabras1, palabras2)

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Detector de Similitud de Textos PDF")
ventana.geometry("400x200")
ventana.configure(bg="#f0f0f0")

instruccion = tk.Label(ventana, text="Haz clic para cargar dos archivos PDF y comparar", bg="#f0f0f0")
instruccion.pack(pady=20)

boton = tk.Button(ventana, text="Seleccionar y Analizar PDFs", command=analizar_textos, bg="#4CAF50", fg="white", font=("Arial", 12))
boton.pack(pady=10)

ventana.mainloop()
