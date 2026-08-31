from flask import Flask, request, make_response
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercise


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/")
def index():
    return {
        "message": "Workout Application API is running"
    }

# WORKOUT ROUTES

@app.route("/workouts", methods=["GET"])
def get_workouts():
    pass

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    pass

@app.route("/workouts", methods=["POST"])
def create_workout():
    pass

@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    pass


# EXERCISE ROUTES

@app.route("/exercises", methods=["GET"])
def get_exercises():
    pass

@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    pass

@app.route("/exercises", methods=["POST"])
def create_exercise():
    pass

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    pass


# WORKOUT EXERCISE ROUTE

@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    pass


if __name__ == "__main__":
    app.run(port=5555, debug=True)