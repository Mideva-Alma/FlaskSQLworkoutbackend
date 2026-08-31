from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema,
    WorkoutSchema,
    WorkoutExerciseSchema
)


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()


@app.route("/")
def index():
    return {
        "message": "Workout Application API is running"
    }

# WORKOUT ROUTES

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)

    if workout is None:
        return {
            "error": "Workout not found"
        }, 404

    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.get_json())

        workout = Workout(
            date=data["date"],
            duration_minutes=data["duration_minutes"],
            notes=data.get("notes")
        )

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as error:
        return {
            "errors": error.messages
        }, 400

    except (ValueError, IntegrityError) as error:
        db.session.rollback()

        return {
            "error": str(error)
        }, 400


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if workout is None:
        return {
            "error": "Workout not found"
        }, 404

    db.session.delete(workout)
    db.session.commit()

    return {
        "message": "Workout deleted successfully"
    }, 200


# EXERCISE ROUTES

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)

    if exercise is None:
        return {
            "error": "Exercise not found"
        }, 404

    return jsonify(exercise_schema.dump(exercise)), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())

        exercise = Exercise(
            name=data["name"],
            category=data["category"],
            equipment_needed=data["equipment_needed"]
        )

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as error:
        return {
            "errors": error.messages
        }, 400

    except (ValueError, IntegrityError) as error:
        db.session.rollback()

        return {
            "error": str(error)
        }, 400


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if exercise is None:
        return {
            "error": "Exercise not found"
        }, 404

    db.session.delete(exercise)
    db.session.commit()

    return {
        "message": "Exercise deleted successfully"
    }, 200


# WORKOUT EXERCISE ROUTE

@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):

    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return {
            "error": "Workout not found"
        }, 404

    if exercise is None:
        return {
            "error": "Exercise not found"
        }, 404

    try:
        request_data = request.get_json() or {}

        data = workout_exercise_schema.load({
            "workout_id": workout_id,
            "exercise_id": exercise_id,
            "reps": request_data.get("reps"),
            "sets": request_data.get("sets"),
            "duration_seconds": request_data.get("duration_seconds")
        })

        workout_exercise = WorkoutExercise(
            workout_id=data["workout_id"],
            exercise_id=data["exercise_id"],
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds")
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify(
            workout_exercise_schema.dump(workout_exercise)
        ), 201

    except ValidationError as error:
        return {
            "errors": error.messages
        }, 400

    except (ValueError, IntegrityError) as error:
        db.session.rollback()

        return {
            "error": str(error)
        }, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)