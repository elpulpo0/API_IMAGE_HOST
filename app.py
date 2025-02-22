from fastapi import FastAPI
from pathlib import Path
import qrcode
from fastapi.staticfiles import StaticFiles

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
    Generate a QR code based on the provided data string.

    Args:
        data (str): The data to encode in the QR code.

    Returns:
        dict: A dictionary containing the URL of the generated QR code image.
    """

    # Create a QRCode object with specific settings
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create the QR code image
    img = qr.make_image(fill="black", back_color="white")

    # Define the file path where the QR code image will be saved
    file_path = UPLOAD_DIR / "qrcode.png"

    # Save the QR code image to the file system
    img.save(file_path)

    # Return the URL of the generated QR code
    return {"url": f"/qr/qrcode.png"}
