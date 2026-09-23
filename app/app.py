from flask import Flask, render_template, jsonify

app = Flask(__name__)


wallpapers = [
    {
        "id": 1,
        "title": "Neon Warrior",
        "category": "Action",
        "image": "https://images.unsplash.com/photo-1578632767115-351597cf2477"
    },
    {
        "id": 2,
        "title": "Midnight Dream",
        "category": "Dark",
        "image": "https://images.unsplash.com/photo-1541562232579-512a21360020"
    },
    {
        "id": 3,
        "title": "Mystic World",
        "category": "Fantasy",
        "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
    },
    {
        "id": 4,
        "title": "Cyber Future",
        "category": "Cyberpunk",
        "image": "https://images.unsplash.com/photo-1519608487953-e999c86e7455"
    },
    {
        "id": 5,
        "title": "Dreamscape",
        "category": "Aesthetic",
        "image": "https://images.unsplash.com/photo-1500534623283-312aade485b7"
    },
    {
        "id": 6,
        "title": "Moonlight",
        "category": "Minimal",
        "image": "https://images.unsplash.com/photo-1519608487953-e999c86e7455"
    }
]


@app.route("/")
def home():
    return render_template("index.html", wallpapers=wallpapers)


@app.route("/api/wallpapers")
def api_wallpapers():
    return jsonify(wallpapers)


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "AnimeVerse"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)