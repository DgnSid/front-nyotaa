import hashlib
import os
import time
import uuid
from urllib.parse import urlparse

import requests
from werkzeug.utils import secure_filename


class CloudinaryService:
    @staticmethod
    def _credentials():
        cloudinary_url = os.getenv("CLOUDINARY_URL", "").strip()
        if cloudinary_url:
            parsed = urlparse(cloudinary_url)
            cloud_name = parsed.hostname
            api_key = parsed.username
            api_secret = parsed.password
            if cloud_name and api_key and api_secret:
                return cloud_name, api_key, api_secret

        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME", "").strip()
        api_key = os.getenv("CLOUDINARY_API_KEY", "").strip()
        api_secret = os.getenv("CLOUDINARY_API_SECRET", "").strip()
        if cloud_name and api_key and api_secret:
            return cloud_name, api_key, api_secret

        raise RuntimeError("Cloudinary credentials are missing")

    @staticmethod
    def _signature(payload, api_secret):
        parts = [f"{key}={payload[key]}" for key in sorted(payload)]
        to_sign = "&".join(parts) + api_secret
        return hashlib.sha1(to_sign.encode("utf-8")).hexdigest()

    @staticmethod
    def upload_raw(file_storage, folder):
        cloud_name, api_key, api_secret = CloudinaryService._credentials()

        filename = secure_filename(file_storage.filename or "document")
        stem, _sep, _ext = filename.rpartition(".")
        if not stem:
            stem = filename

        timestamp = int(time.time())
        public_id = f"{stem}-{uuid.uuid4().hex[:12]}"
        signature_payload = {
            "folder": folder,
            "public_id": public_id,
            "timestamp": timestamp,
        }
        signature = CloudinaryService._signature(signature_payload, api_secret)

        upload_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/raw/upload"
        file_storage.stream.seek(0)
        response = requests.post(
            upload_url,
            data={
                "api_key": api_key,
                "timestamp": timestamp,
                "folder": folder,
                "public_id": public_id,
                "signature": signature,
            },
            files={
                "file": (
                    filename,
                    file_storage.stream,
                    file_storage.mimetype or "application/octet-stream",
                )
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
