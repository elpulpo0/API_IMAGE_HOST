# Utiliser une image Python de base plus récente
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le conteneur
COPY . .

# Créer un utilisateur non-root et changer le propriétaire des fichiers
RUN useradd -ms /bin/bash appuser && chown -R appuser /app
USER appuser

# Exposer le port que votre application va utiliser
EXPOSE 8000

# Définir la commande par défaut pour exécuter l'application avec uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "warning"]