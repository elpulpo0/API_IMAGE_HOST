
# QR Code Generator API for MultiversX Plugin (ElizaOS)

This repository provides a simple FastAPI-based API for generating QR codes. It was created to be used as part of the **MultiversX plugin** for **Eliza**.

The API allows users to generate a QR code image from any given string, and the generated image is saved in a publicly accessible directory, allowing it to be retrieved via a URL.

## Features

- **QR Code Generation**: Generate QR codes based on any string of data.
- **Static File Hosting**: The generated QR codes are saved to the server and served as static files, making them accessible via a public URL.
- **Easy Integration**: Designed to be easily integrated with the MultiversX plugin of Eliza.

## API Endpoints

### `POST /generate_qr/`

This endpoint accepts a string of data, generates a QR code for it, and returns a URL where the generated QR code image can be accessed.

#### Request Body

```json
{
  "data": "string_to_encode"
}
```

- **data**: The string that you want to encode into a QR code.

#### Response

```json
{
  "url": "/uploads/qrcode.png"
}
```

- **url**: A relative URL pointing to the generated QR code image. The image will be accessible at this URL after the QR code is generated.

### Example Request

To generate a QR code, send a POST request to `/generate_qr/` with a string to encode. Here's an example using `curl`:

```bash
curl -X 'POST'   'http://localhost:3001/generate_qr/'   -H 'Content-Type: application/json'   -d '{"data": "example_data_to_encode"}'
```

### Example Response

```json
{
  "url": "/uploads/qrcode.png"
}
```

The QR code image will be saved in the `uploads` folder and can be accessed via the URL `http://localhost:3001/uploads/qrcode.png`.

## Installation and Setup

### Prerequisites

To run this API locally, you need to have the following installed:

- Python 3.7+
- FastAPI
- Uvicorn
- qrcode

You can install the required dependencies with `pip`:

```bash
pip install -r requirements.txt
```

### Running the API

To run the API locally, use Uvicorn to serve the FastAPI app:

```bash
uvicorn app:app --reload
```

This will start the API on `http://localhost:8000` by default.

### Directory Structure

```
.
├── uploads/              # The directory where QR code images are saved
├── app.py               # FastAPI app with the QR code generation endpoint
└── requirements.txt      # Python dependencies
```

### Accessing Generated QR Codes

After generating a QR code, the image will be stored in the `uploads` directory. You can access the generated QR code via the URL returned in the response.

For example, if your server is running on `localhost:3001`, the QR code image will be available at:

```
http://localhost:3001/uploads/qrcode.png
```

## Usage with MultiversX Plugin

This QR code generator API is designed to be used as part of the MultiversX plugin for Eliza, specifically with the RECEIVE_EGLD action, where it generates a dedicated xPortal QR Code. It also enables seamless QR code generation for any data that needs to be encoded, making it useful for wallet addresses, transactions, or other use cases within the MultiversX ecosystem.

## License

This project is licensed under the MIT License.
