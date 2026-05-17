from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "fittrack-secret-key"

workouts = []


def check_api_key(req):
    api_key = req.headers.get("X-API-Key")
    return api_key == API_KEY


@app.route("/api/workouts", methods=["POST"])
def create_workout():
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    if not data or "title" not in data or "duration" not in data:
        return jsonify({"error": "Invalid data"}), 400

    workout = {
        "id": len(workouts) + 1,
        "title": data["title"],
        "duration": data["duration"]
    }

    workouts.append(workout)

    return jsonify(workout), 201


@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(workouts)


@app.route("/api/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    global workouts

    workouts = [
        workout for workout in workouts
        if workout["id"] != workout_id
    ]

    return jsonify({"message": "Workout deleted"})


if __name__ == "__main__":
    app.run(debug=True)