from fastapi import FastAPI
from pathlib import Path
import qrcode
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime
from fastapi import Request

# Create FastAPI app instance
app = FastAPI()

# Define the upload directory where QR codes will be saved
UPLOAD_DIR = Path("images")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount the static file directory to serve the QR code images
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
def home():
    return {"message": "QR Code API is running!"}

# Endpoint to generate the QR code
@app.post("/generate_qr/")
async def generate_qr(data: str):
    """
    Generate a QR code and return a preview link with metadata.
    """

    # Générer un nom de fichier unique basé sur un timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"qrcode_{timestamp}.png"
    file_path = UPLOAD_DIR / filename

    # Create and save the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(file_path)

    # Return a preview link
    return {"preview_url": f"/images/{filename}"}


# Endpoint to serve the HTML preview page with metadata
@app.get("/qr/{filename}", response_class=HTMLResponse)
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
        <!-- HTML Meta Tags -->
        <title>Scan Me</title>
        <meta name="description" content="">

        <!-- Facebook Meta Tags -->
        <meta property="og:url" content="{base_url}/preview/{filename}">
        <meta property="og:type" content="website">
        <meta property="og:title"  content="Scan Me">
        <meta property="og:description" content="Scan Me">
        <meta property="og:image" content="{image_url}">
        <meta property="og:image:type" content="image/png">
        <meta property="og:image:width" content="500">
        <meta property="og:image:height" content="500">

        <!-- Twitter Meta Tags -->
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
