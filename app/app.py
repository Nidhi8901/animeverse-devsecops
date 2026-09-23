from flask import Flask, render_template, jsonify, send_from_directory
from pathlib import Path
from urllib.parse import quote

app = Flask(__name__)

IMAGE_ROOT = Path(app.root_path) / "static" / "images"

ANIME_CATEGORIES = {
    "demon-slayer": "Demon Slayer",
    "jujutsu-kaisen": "Jujutsu Kaisen",
    "tokyo-revengers": "Tokyo Revengers",
    "wind-breaker": "Wind Breaker"
}

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


def get_wallpapers():
    wallpapers = []
    wallpaper_id = 1

    for folder_name, category_name in ANIME_CATEGORIES.items():

        folder_path = IMAGE_ROOT / folder_name

        if not folder_path.exists():
            continue

        files = sorted([
            file
            for file in folder_path.iterdir()
            if file.is_file()
            and file.suffix.lower() in ALLOWED_EXTENSIONS
        ])

        for number, file in enumerate(files, start=1):

            wallpapers.append({
                "id": wallpaper_id,
                "title": f"{category_name} Wallpaper {number}",
                "category": category_name,
                "image": f"/static/images/{folder_name}/{quote(file.name)}",
                "download_url": f"/download/{folder_name}/{quote(file.name)}"
            })

            wallpaper_id += 1

    return wallpapers


@app.route("/")
def home():
    return render_template(
        "index.html",
        wallpapers=get_wallpapers()
    )


@app.route("/api/wallpapers")
def api_wallpapers():
    return jsonify(get_wallpapers())


@app.route("/download/<category>/<path:filename>")
def download_wallpaper(category, filename):

    if category not in ANIME_CATEGORIES:
        return "Invalid category", 404

    folder_path = IMAGE_ROOT / category

    return send_from_directory(
        folder_path,
        filename,
        as_attachment=True
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "AnimeVerse"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )