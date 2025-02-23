from fastapi import FastAPI, Request
from pathlib import Path
import qrcode
import logging
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime
from PIL import Image

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create FastAPI app instance
app = FastAPI(
    title="QR Code Generator API",
    description="An API to generate QR codes and preview them with Open Graph metadata.",
    contact={
        "name": "El Pulpo",
        "url": "https://qrcode-api.elpulpo.xyz",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Define the upload directory where QR codes will be saved
UPLOAD_DIR = Path("images")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount the static file directory to serve the QR code images
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/", tags=["QR Code Generator"])
def home():
    return {"message": "QR Code API is running!"}


# Endpoint to generate the QR code
@app.post("/generate_qr/", tags=["QR Code Generator"])
async def generate_qr(data: str):
    """
    Generate a QR code and return a preview link with metadata.
    """
    logging.info(f"Data received for QR generation: {data}")

    # Générer un nom de fichier unique basé sur un timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"qrcode_{timestamp}.png"
    file_path = UPLOAD_DIR / filename

    # Créer et enregistrer le QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image(fill="black", back_color="white").convert("RGBA")

    # Définir la taille finale de l'image (1200x630)
    final_width = 1200
    final_height = 630
    qr_size = 500

    # Créer une nouvelle image blanche (ou autre couleur de fond)
    background = Image.new("RGBA", (final_width, final_height), "white")

    # Calculer les coordonnées pour centrer le QR Code
    x_offset = (final_width - qr_size) // 2
    y_offset = (final_height - qr_size) // 2

    # Redimensionner le QR Code à 500x500
    img_qr = img_qr.resize((qr_size, qr_size), Image.LANCZOS)

    # Coller le QR Code au centre de l’image
    background.paste(img_qr, (x_offset, y_offset), img_qr)

    # Sauvegarder l’image finale
    background.save(file_path)

    # Compter le nombre d'images dans le dossier
    num_images = len(list(UPLOAD_DIR.glob("*.png")))
    logging.info(
        f"QR Code generated and saved as {filename}. Total images in folder: {num_images}"
    )

    return {"preview_url": f"/qr/{filename}"}


# Endpoint to delete all QR codes
@app.delete("/delete_qrs/", tags=["QR Code Generator"])
def delete_qrs():
    """
    Delete all QR code images from the folder.
    """
    num_deleted = 0
    for file in UPLOAD_DIR.glob("*.png"):
        file.unlink()
        num_deleted += 1
    logging.info(f"Deleted {num_deleted} QR codes from the folder.")
    return {"message": f"Deleted {num_deleted} QR codes."}


# Endpoint to serve the HTML preview page with metadata
@app.get("/qr/{filename}", response_class=HTMLResponse, tags=["QR Code Generator"])
async def preview_qr(request: Request, filename: str):
    """
    Generate an HTML page with Open Graph metadata for preview.
    """
    base_url = str(request.base_url).rstrip("/")
    image_url = f"{base_url}/images/{filename}"
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Scan Me</title>
        <meta name="description" content="">
        <meta property="og:url" content="{base_url}/preview/{filename}">
        <meta property="og:type" content="website">
        <meta property="og:title"  content="Scan Me">
        <meta property="og:description" content="Scan Me">
        <meta property="og:image" content="{image_url}">
        <meta property="og:image:type" content="image/png">
        <meta property="og:image:width" content="1200">
        <meta property="og:image:height" content="630">
        <meta name="twitter:card" content="summary_large_image">
        <meta property="twitter:domain" content="elpulpo.xyz">
        <meta property="twitter:url" content="{base_url}/preview/{filename}">
        <meta name="twitter:title" content="Scan Me">
        <meta name="twitter:description" content="Scan Me">
        <meta name="twitter:image" content="{image_url}">
    </head>
    <body>
        <img src="{image_url}" alt="QR Code">
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
