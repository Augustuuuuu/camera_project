from PyPDF2 import PdfReader, PdfWriter
import math

A4_WIDTH = 595  # points
A4_HEIGHT = 842  # points

def process_pdf(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        # Get original dimensions
        orig_width = float(page.mediabox.width)
        orig_height = float(page.mediabox.height)
        
        # Calcular o fator de escala para que a largura caiba em A4
        # e a altura seja distribuída em duas páginas
        scale_width = A4_WIDTH / orig_width
        scale_height = (2 * A4_HEIGHT) / orig_height
        scale_factor = min(scale_width, scale_height)
        
        # Escalar a página
        page.scale(scale_factor, scale_factor)
        
        # Adicionar a página ao documento
        writer.add_page(page)
        
        # Adicionar uma página em branco para a segunda parte
        writer.add_blank_page(width=A4_WIDTH, height=A4_HEIGHT)

    # Salvar o resultado
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

if __name__ == "__main__":
    process_pdf("backend.pdf", "backend_a4.pdf")