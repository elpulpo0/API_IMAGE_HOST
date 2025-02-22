from fastapi import FastAPI
from pathlib import Path
import qrcode
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# Create FastAPI app instance
app = FastAPI()

# Define the upload directory where QR codes will be saved
UPLOAD_DIR = Path("qr")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount the static file directory to serve the QR code images
app.mount("/qr", StaticFiles(directory="qr"), name="qr")

# Endpoint to generate the QR code
@app.post("/generate_qr/")
async def generate_qr(data: str):
    """
    Generate a QR code and return a preview link with metadata.
    """

    # Generate a unique filename based on the data
    filename = "qrcode.png"
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
    return {"preview_url": f"/preview/{filename}"}

# Endpoint to serve the HTML preview page with metadata
@app.get("/preview/{filename}", response_class=HTMLResponse)
async def preview_qr(filename: str):
    """
    Generate an HTML page with Open Graph metadata for preview.
    """
    image_url = f"/qr/{filename}"
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>QR Code Preview</title>

        <!-- Open Graph metadata -->
        <meta property="og:title" content="QR Code Preview">
        <meta property="og:description" content="Scan me">
        <meta property="og:image" content="{image_url}">
        <meta property="og:image:type" content="image/png">
        <meta property="og:image:width" content="500">
        <meta property="og:image:height" content="500">
        <meta property="og:type" content="website">
        <meta property="og:url" content="{image_url}">
    </head>
    <body>
        <img src="{image_url}" alt="QR Code">
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

