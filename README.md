# Καταγραφή Προπονήσεων

Η Καταγραφή Προπονήσεων είναι μια απλή εφαρμογή για καταγραφή προπονήσεων, ασκήσεων και επιδόσεων.

Ως θέμα εργασίας επέλεξα την ανάπτυξη ενός progress tracker για προπονήσεις, επειδή είναι μια εφαρμογή που μπορεί να μου φανεί χρήσιμη στην καθημερινή καταγραφή της προπόνησής μου.

Η εφαρμογή δημιουργήθηκε με FastAPI, SQLAlchemy και SQLite.

## Λειτουργίες

- Δημιουργία, προβολή, επεξεργασία και διαγραφή προπονήσεων
- Δημιουργία, προβολή, επεξεργασία και διαγραφή ασκήσεων
- Καταγραφή επιδόσεων με sets, reps και βάρος
- Προβολή βασικών στατιστικών προπόνησης
- In-memory cache για τα στατιστικά
- Validation των δεδομένων εισόδου
- Error handling για περιπτώσεις όπου δεν υπάρχει κάποια εγγραφή
- Απλό frontend για προβολή προπονήσεων, ασκήσεων και στατιστικών
- Basic API tests

## Τεχνολογίες

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- HTML
- Pytest

## Βάση δεδομένων

Η βάση δεδομένων περιλαμβάνει τρεις βασικούς πίνακες:

- `προπονησεις`
- `ασκησεις`
- `επιδόσεις`

Ο πίνακας `επιδόσεις` συνδέει τις προπονήσεις με τις ασκήσεις και αποθηκεύει τα sets, τις επαναλήψεις και το βάρος.

Στα foreign keys `workout_id` και `exercise_id` χρησιμοποιούνται indexes.

## Σημείωση ανάπτυξης

Κατά την ανάπτυξη της εφαρμογής τη δοκίμαζα τοπικά σε Fedora Linux και υπήρχε ήδη το αρχείο SQLite `gym_logger.db` με τους πίνακες δημιουργημένους.

Για αυτό η απουσία του `Base.metadata.create_all()` δεν δημιούργησε άμεσα πρόβλημα στο τοπικό μου περιβάλλον. Αργότερα πρόσθεσα την εντολή ώστε οι πίνακες να δημιουργούνται αυτόματα και σε καθαρή εγκατάσταση της εφαρμογής.

## Εγκατάσταση

### Linux / macOS

Δημιουργία virtual environment:

```bash
python3 -m venv venv
### Windows

Δημιουργία virtual environment:

```bash
python -m venv venv
```

Ενεργοποίηση:

```bash
venv\Scripts\activate
```

## Εγκατάσταση dependencies

```bash
pip install -r requirements.txt
```

## Εκτέλεση εφαρμογής

```bash
uvicorn app.main:app --reload
```

Η εφαρμογή είναι διαθέσιμη στο:

```text
http://127.0.0.1:8000
```

Το Swagger API documentation είναι διαθέσιμο στο:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Workouts

```text
GET    /workouts/
GET    /workouts/{id}
POST   /workouts/
PUT    /workouts/{id}
DELETE /workouts/{id}
```

### Exercises

```text
GET    /exercises/
GET    /exercises/{id}
POST   /exercises/
PUT    /exercises/{id}
DELETE /exercises/{id}
```

### Performances

```text
GET  /performances/
POST /performances/
```

### Stats

```text
GET /stats/
```

## Validation

Η εφαρμογή πραγματοποιεί βασικό validation στα δεδομένα εισόδου.

- ο τίτλος προπόνησης δεν μπορεί να είναι κενός
- το όνομα άσκησης δεν μπορεί να είναι κενό
- η ημερομηνία πρέπει να έχει μορφή `YYYY-MM-DD`
- τα sets και τα reps πρέπει να είναι μεγαλύτερα από το μηδέν
- το βάρος δεν μπορεί να είναι αρνητικό

## Cache

Το endpoint `/stats/` χρησιμοποιεί απλή in-memory cache διάρκειας 30 δευτερολέπτων.

## Tests

Για την εκτέλεση των tests:

```bash
python -m pytest testakia -v
```

Τα tests ελέγχουν βασικά endpoints, validation, περιπτώσεις 404 και τη διαγραφή προπονήσεων ή ασκήσεων με συνδεδεμένες επιδόσεις.

## Frontend

Η εφαρμογή περιλαμβάνει ένα απλό frontend στο `static/index.html`.

Από την αρχική σελίδα εμφανίζονται:

- οι προπονήσεις
- οι ασκήσεις
- τα βασικά στατιστικά
