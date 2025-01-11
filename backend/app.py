from flask import Flask, jsonify, request, send_from_directory

from scripts.search_querry import get_top_matches

from scripts.organize_and_sentence_transform import main_call, check_required_file

from scripts.model_downloader import (
    download_cross_encoder,
    download_sentence_transformer,
)


download_cross_encoder()
download_sentence_transformer()

app = Flask(__name__)


@app.route("/")
def serve_index():
    return send_from_directory("../frontend", "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("../frontend", path)


@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()
    if check_required_file():
        return jsonify(
            {"error": "Required data file is missing. Please fetch the data first."}
        ), 428
    if not query:
        return jsonify({"error": "No query provided"}), 400
    print("starting a search")
    raw_result = get_top_matches(query)
    results = [
        {
            "url": item["link"],
            "title": item["title"],
            "description": item["summary"],
        }
        for item in raw_result
    ]

    return jsonify(results)


@app.route("/api/update_dataset", methods=["GET"])
def fetch_data():
    main_call()
    return jsonify({"data": "Fetched data from Python backend!"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
