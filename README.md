# Flask SQLAlchemy Workout Application Backend

## Project Description

This project is a RESTful backend API for a workout tracking application.

The application allows users to create, view, and delete workouts and exercises. Exercises can be associated with workouts through workout exercises, allowing the application to record sets, repetitions, and duration.

The backend is built using Flask, SQLAlchemy, Flask-Migrate, Marshmallow, and SQLite.

## Technologies

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Marshmallow
* SQLite
* Pipenv
* Pytest

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Mideva-Alma/FlaskSQLworkoutbackend.git
cd FlaskSQLworkoutbackend
```

### 2. Install dependencies

This project uses Pipenv.

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

### 3. Set up the database

Run the existing database migrations:

```bash
flask --app server/app.py db upgrade
```

### 4. Seed the database

Populate the database with sample exercises, workouts, and workout exercises:

```bash
python server/seed.py
```

## Running the Application

Start the Flask development server:

```bash
flask --app server/app.py run
```

The API will be available at:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Workouts

#### GET /workouts

Returns all workouts.

```text
GET /workouts
```

#### GET /workouts/<id>

Returns a single workout by ID.

```text
GET /workouts/1
```

#### POST /workouts

Creates a new workout.

Example request:

```json
{
  "date": "2026-09-14",
  "duration_minutes": 45,
  "notes": "Upper body workout"
}
```

```text
POST /workouts
```

#### DELETE /workouts/<id>

Deletes a workout by ID.

```text
DELETE /workouts/1
```

### Exercises

#### GET /exercises

Returns all exercises.

```text
GET /exercises
```

#### GET /exercises/<id>

Returns a single exercise by ID.

```text
GET /exercises/1
```

#### POST /exercises

Creates a new exercise.

Example request:

```json
{
  "name": "Push Ups",
  "category": "Chest",
  "equipment_needed": false
}
```

```text
POST /exercises
```

#### DELETE /exercises/<id>

Deletes an exercise by ID.

```text
DELETE /exercises/1
```

### Workout Exercises

#### POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises

Associates an exercise with a workout and records workout details.

Example:

```json
{
  "reps": 12,
  "sets": 3,
  "duration_seconds": 60
}
```

```text
POST /workouts/1/exercises/1/workout_exercises
```

## Validation

The API uses validation at multiple levels.

### Database Table Constraints

The database uses constraints such as:

* Primary keys
* Foreign keys
* Non-null constraints
* Unique constraints where required

### Model Validation

SQLAlchemy model validation prevents invalid values such as:

* Negative workout durations
* Negative repetitions
* Negative sets
* Negative exercise duration

### Schema Validation

Marshmallow validates incoming API data before it is saved to the database.

Examples include:

* Required fields
* Minimum string lengths
* Non-negative numeric values
* Correct data types

Invalid data returns an appropriate validation error instead of being saved.

## Database

The application uses SQLite as its database.

Database migrations are managed using Flask-Migrate and Alembic.

To apply migrations:

```bash
flask --app server/app.py db upgrade
```

To create a new migration after changing the models:

```bash
flask --app server/app.py db migrate -m "describe changes"
```

Then apply it:

```bash
flask --app server/app.py db upgrade
```

## Testing

The project includes API tests using Pytest.

Run the tests with:

```bash
python -m pytest
```

## Project Structure

```text
FlaskSQLworkoutbackend/
│
├── migrations/
│   ├── versions/
│   └── ...
│
├── server/
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   └── tests/
│       └── test_api.py
│
├── .gitignore
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Error Handling

The API returns appropriate HTTP status codes for successful requests, missing resources, invalid input, and database errors.

Examples include:

* `200 OK` for successful GET requests
* `201 Created` for successful POST requests
* `204 No Content` for successful DELETE requests
* `400 Bad Request` for invalid input
* `404 Not Found` when a requested resource does not exist

## Relationships

The application uses SQLAlchemy relationships between:

* Workouts and WorkoutExercises
* Exercises and WorkoutExercises
* Workouts and Exercises through WorkoutExercise

This allows workouts to contain multiple exercises and exercises to be reused across multiple workouts.
