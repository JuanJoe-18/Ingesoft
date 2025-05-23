import os
from docx import Document
import pdfplumber
from markdownify import markdownify as md
import tkinter as tk
from tkinter import filedialog, messagebox

def docx_to_markdown(docx_path):
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    text = '\n'.join(full_text)
    return md(text)

def pdf_to_markdown(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return md(text)

def convert_to_markdown(input_path, output_path):
    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".docx":
        md_content = docx_to_markdown(input_path)
    elif ext == ".pdf":
        md_content = pdf_to_markdown(input_path)
    else:
        raise ValueError("Formato no soportado. Usa .docx o .pdf")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    messagebox.showinfo("Conversor", "Selecciona uno o varios archivos de entrada (.docx o .pdf)")
    input_paths = filedialog.askopenfilenames(
        title="Selecciona los archivos de entrada",
        filetypes=[("Documentos Word", "*.docx"), ("Archivos PDF", "*.pdf")]
    )
    if not input_paths:
        messagebox.showerror("Error", "No se seleccionaron archivos de entrada.")
        exit(1)

    messagebox.showinfo("Conversor", "Selecciona la carpeta donde se guardarán los archivos Markdown")
    output_folder = filedialog.askdirectory(
        title="Selecciona la carpeta de destino"
    )
    if not output_folder:
        messagebox.showerror("Error", "No se seleccionó la carpeta de destino.")
        exit(1)

    errores = []
    for input_path in input_paths:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_folder, base_name + ".md")
        try:
            convert_to_markdown(input_path, output_path)
        except Exception as e:
            errores.append(f"{os.path.basename(input_path)}: {e}")

    if errores:
        messagebox.showerror("Errores", "Algunos archivos no se pudieron convertir:\n" + "\n".join(errores))
    else:
        messagebox.showinfo("Éxito", "✅ Todos los archivos fueron convertidos exitosamente en:\n" + output_folder)