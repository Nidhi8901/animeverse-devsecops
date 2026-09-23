import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.app import app


def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"AnimeVerse" in response.data


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"
    assert data["application"] == "AnimeVerse"


def test_wallpapers_api():
    client = app.test_client()

    response = client.get("/api/wallpapers")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_wallpaper_structure():
    client = app.test_client()

    response = client.get("/api/wallpapers")

    data = response.get_json()

    wallpaper = data[0]

    assert "id" in wallpaper
    assert "title" in wallpaper
    assert "category" in wallpaper
    assert "image" in wallpaper