from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            error="Exercise name must be at least 2 characters long."
        )
    )

    category = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            error="Exercise category must be at least 2 characters long."
        )
    )

    equipment_needed = fields.Bool(required=True)

    workouts = fields.Nested(
        "WorkoutSchema",
        many=True,
        dump_only=True,
        exclude=("exercises", "workout_exercises")
    )

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(
            min=0,
            error="Reps cannot be negative."
        )
    )

    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(
            min=0,
            error="Sets cannot be negative."
        )
    )

    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(
            min=0,
            error="Duration cannot be negative."
        )
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(
            min=0,
            error="Workout duration cannot be negative."
        )
    )

    notes = fields.Str(allow_none=True)

    exercises = fields.Nested(
        ExerciseSchema,
        many=True,
        dump_only=True
    )

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )