from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    print("Clearing existing data...")

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Creating exercises...")

    exercises = [
        Exercise(
            name="Push-ups",
            category="Strength",
            equipment_needed=False
        ),
        Exercise(
            name="Squats",
            category="Strength",
            equipment_needed=False
        ),
        Exercise(
            name="Bench Press",
            category="Strength",
            equipment_needed=True
        ),
        Exercise(
            name="Running",
            category="Cardio",
            equipment_needed=False
        ),
        Exercise(
            name="Cycling",
            category="Cardio",
            equipment_needed=True
        ),
    ]

    db.session.add_all(exercises)
    db.session.commit()

    print("Creating workouts...")

    workout1 = Workout(
        date=date(2026, 8, 25),
        duration_minutes=45,
        notes="Upper body strength workout"
    )

    workout2 = Workout(
        date=date(2026, 8, 27),
        duration_minutes=60,
        notes="Lower body and cardio workout"
    )

    workout3 = Workout(
        date=date(2026, 8, 29),
        duration_minutes=30,
        notes="Quick cardio session"
    )

    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()

    print("Creating workout exercises...")

    workout_exercises = [
        WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=exercises[0].id,
            reps=15,
            sets=3,
            duration_seconds=None
        ),
        WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=exercises[2].id,
            reps=10,
            sets=4,
            duration_seconds=None
        ),
        WorkoutExercise(
            workout_id=workout2.id,
            exercise_id=exercises[1].id,
            reps=12,
            sets=4,
            duration_seconds=None
        ),
        WorkoutExercise(
            workout_id=workout2.id,
            exercise_id=exercises[3].id,
            reps=None,
            sets=None,
            duration_seconds=1800
        ),
        WorkoutExercise(
            workout_id=workout3.id,
            exercise_id=exercises[4].id,
            reps=None,
            sets=None,
            duration_seconds=1500
        ),
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print("Database seeded successfully!")