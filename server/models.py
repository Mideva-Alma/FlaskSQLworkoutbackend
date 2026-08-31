from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint


db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    category = db.Column(
        db.String,
        nullable=False
    )

    equipment_needed = db.Column(
        db.Boolean,
        nullable=False
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty.")

        if len(value.strip()) < 2:
            raise ValueError(
                "Exercise name must contain at least 2 characters."
            )

        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise category cannot be empty.")

        return value.strip()


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(
        db.Date,
        nullable=False
    )

    duration_minutes = db.Column(
        db.Integer,
        nullable=False
    )

    notes = db.Column(
        db.Text
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True
    )

    __table_args__ = (
        CheckConstraint(
            "duration_minutes >= 0",
            name="check_workout_duration_non_negative"
        ),
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None:
            raise ValueError("Workout duration is required.")

        if value < 0:
            raise ValueError(
                "Workout duration cannot be negative."
            )

        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    reps = db.Column(db.Integer)

    sets = db.Column(db.Integer)

    duration_seconds = db.Column(db.Integer)

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    __table_args__ = (
        CheckConstraint(
            "reps IS NULL OR reps >= 0",
            name="check_reps_non_negative"
        ),
        CheckConstraint(
            "sets IS NULL OR sets >= 0",
            name="check_sets_non_negative"
        ),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds >= 0",
            name="check_duration_seconds_non_negative"
        ),
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_workout_exercise"
        ),
    )

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value < 0:
            raise ValueError("Reps cannot be negative.")

        return value

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value < 0:
            raise ValueError("Sets cannot be negative.")

        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and value < 0:
            raise ValueError(
                "Duration cannot be negative."
            )

        return value