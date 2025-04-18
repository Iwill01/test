from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables frontend requests from different origin

MAX_VOTES = 10

votes = {
    "A": 0,
    "B": 0,
    "total": 0
}

valid_codes = {"user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"}
used_codes = set()
admin_codes = {"admin123"}

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    code = data.get("code")

    if code in admin_codes:
        if votes["A"] == votes["B"]:
            winner = "Tie"
        else:
            winner = "A" if votes["A"] > votes["B"] else "B"

        return jsonify({
            "admin": True,
            "votes": {
                "A": votes["A"],
                "B": votes["B"]
            },
            "winner": winner,
            "message": "Admin access granted."
        })

    if code in used_codes:
        return jsonify({"success": False, "message": "Code already used."})

    if code in valid_codes:
        used_codes.add(code)
        return jsonify({"success": True, "message": "Code verified. You can vote now."})
    else:
        return jsonify({"success": False, "message": "Invalid code."})

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    choice = data.get("choice")

    if choice in votes and votes["total"] < MAX_VOTES:
        votes[choice] += 1
        votes["total"] += 1
        return jsonify({"message": f"Vote for {choice} submitted."})
    else:
        return jsonify({"message": "Invalid vote or vote limit reached."})

@app.route('/stats', methods=['POST'])
def stats():
    data = request.get_json()
    code = data.get("code")
    total = votes["total"]
    percent_casted = round((total / MAX_VOTES) * 100, 1)

    if code in admin_codes:
        percent_a = round((votes["A"] / total) * 100, 1) if total else 0
        percent_b = round((votes["B"] / total) * 100, 1) if total else 0

        return jsonify({
            "total_votes": total,
            "percent_casted": percent_casted,
            "percent_A": percent_a,
            "percent_B": percent_b
        })
    else:
        return jsonify({
            "total_votes": total,
            "percent_casted": percent_casted
        })

if __name__ == '__main__':
    app.run(debug=True)
