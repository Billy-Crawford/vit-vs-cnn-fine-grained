import io
import sys
import os

import pytest
from fastapi.testclient import TestClient
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def _fake_image_bytes(fmt="JPEG"):
    buffer = io.BytesIO()
    Image.new("RGB", (64, 64), color=(120, 130, 90)).save(buffer, format=fmt)
    buffer.seek(0)
    return buffer


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "vit" in body["models_loaded"]
    assert "resnet" in body["models_loaded"]


def test_classes_returns_200_entries(client):
    response = client.get("/classes")
    assert response.status_code == 200
    assert len(response.json()) == 200


def test_predict_valid_image(client):
    img = _fake_image_bytes("JPEG")
    response = client.post("/predict", files={"file": ("test.jpg", img, "image/jpeg")})
    assert response.status_code == 200
    body = response.json()
    for model_key in ("vit", "resnet"):
        assert model_key in body
        assert len(body[model_key]["top3"]) == 3


def test_predict_rejects_invalid_content_type(client):
    fake_text = io.BytesIO(b"not an image")
    response = client.post("/predict", files={"file": ("test.txt", fake_text, "text/plain")})
    assert response.status_code == 400


def test_predict_rejects_corrupted_image(client):
    corrupted = io.BytesIO(b"\xff\xd8\xff\x00garbage-not-a-real-jpeg")
    response = client.post("/predict", files={"file": ("test.jpg", corrupted, "image/jpeg")})
    assert response.status_code == 400


def test_attention_returns_base64_png(client):
    img = _fake_image_bytes("PNG")
    response = client.post("/attention", files={"file": ("test.png", img, "image/png")})
    assert response.status_code == 200
    assert len(response.json()["attention_overlay_base64"]) > 0