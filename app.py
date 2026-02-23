from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from scraper import fetch_tenders_for_district

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tenders")
def get_tenders():
    district = request.args.get("district", "Nabarangpur")

    try:
        tenders = fetch_tenders_for_district(district)
        return jsonify({"district": district, "count": len(tenders), "tenders": tenders})
    except Exception as exc:  # noqa: BLE001
        return (
            jsonify(
                {
                    "district": district,
                    "error": "Unable to fetch tenders from source website in current environment.",
                    "details": str(exc),
                    "tenders": [],
                }
            ),
            502,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
