from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import yellow, red, black,white
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.graphics import shapes, barcode

import json
import io
import PIL

def load(type):

    # Configuración de canva
    pageWidth, pageHeight = letter
    pageHeight = pageHeight / 2
    page = canvas.Canvas("hello.pdf", pagesize=(pageWidth, pageHeight))
