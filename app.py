from fastapi import FastAPI, HTTPException
from pathlib import Path
import qrcode
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Monter le répertoire /uploads pour servir les fichiers statiques
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.post("/generate_qr/")
async def generate_qr(data: str):
    """Génère un QR code à partir de la donnée et le sauvegarde dans un fichier."""

    # Générer l'image QR code à partir des données
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Créer l'image du QR code
    img = qr.make_image(fill="black", back_color="white")

    # Définir le chemin de l'image
    file_path = UPLOAD_DIR / "qrcode.png"

    # Sauvegarder l'image dans le dossier uploads
    img.save(file_path)

    # Retourner l'URL de l'image générée
    return {"url": f"/uploads/qrcode.png"}
