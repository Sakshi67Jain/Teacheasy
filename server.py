from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.distance import geodesic
import time  

app = Flask(__name__)
CORS(app)

teacher_location = None  
attendance_end_time = None  

@app.route("/set_location", methods=["POST"])
def set_location():
    global teacher_location
    data = request.json
    teacher_location = (data["latitude"], data["longitude"])
    return jsonify({"message": "✅ Teacher location set!"})

@app.route("/start_attendance", methods=["POST"])
def start_attendance():
    global attendance_end_time
    data = request.json
    duration = int(data["duration"])  
    attendance_end_time = time.time() + duration  
    return jsonify({"message": f"✅ Attendance started for {duration // 60} minute(s)!"})

@app.route("/get_attendance_status", methods=["GET"])
def get_attendance_status():
    global attendance_end_time
    if attendance_end_time is None:
        return jsonify({"status": "❌ Attendance not started!", "time_left": 0}), 400

    time_left = max(0, int(attendance_end_time - time.time()))
    print(f"📢 Attendance Time Left: {time_left}s")  # ✅ DEBUG LOG

    if time_left == 0:
        return jsonify({"status": "⏳ Attendance time over!", "time_left": 0})
    
    return jsonify({"status": f"⏳ Time left: {time_left}s", "time_left": time_left})

@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    global teacher_location, attendance_end_time
    if teacher_location is None:
        return jsonify({"error": "❌ Teacher location not set!"}), 400
    if attendance_end_time is None or time.time() > attendance_end_time:
        return jsonify({"error": "❌ Attendance time over!"}), 400

    data = request.json
    student_location = (data["latitude"], data["longitude"])
    distance = geodesic(teacher_location, student_location).meters

    if distance <= 50:
        return jsonify({"message": "✅ Attendance Marked!"})
    else:
        return jsonify({"error": f"❌ Too far! {distance:.2f}m away!"})

if __name__ == "_main_":
    app.run(debug=True)