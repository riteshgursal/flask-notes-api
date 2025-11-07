# RESTful Notes API (Flask & MongoDB)

This project is a backend RESTful API for a simple note-taking application. It is built with Python, Flask, and MongoDB (using MongoDB Atlas for cloud database hosting).

The API provides full **CRUD** (Create, Read, Update, Delete) functionality for notes and is documented for testing with Postman.

**Project Status:** Completed

---

## 🚀 Tech Stack

* **Backend:** Flask (Python)
* **Database:** MongoDB (hosted on MongoDB Atlas)
* **API Testing:** Postman
* **Python Driver:** PyMongo

---

## 🛠️ Features

* **Create Note:** Add a new note (title, content) to the database.
* **Read All Notes:** Retrieve a list of all notes.
* **Read One Note:** Retrieve a single note by its unique ID.
* **Update Note:** Modify the title/content of an existing note.
* **Delete Note:** Remove a note from the database.
* **JSON-based:** All requests and responses use the JSON format.
* **Error Handling:** Provides clear JSON error messages for bad requests or missing notes.

---

## 📡 API Endpoints (Demo)

The API runs locally on `http://127.0.0.1:5000`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/notes` | Creates a new note. Requires a JSON body. |
| `GET` | `/notes` | Retrieves all notes in the database. |
| `GET` | `/notes/<id>` | Retrieves a single note by its `_id`. |
| `PUT` | `/notes/<id>` | Updates an existing note. Requires a JSON body. |
| `DELETE` | `/notes/<id>` | Deletes a note by its `_id`. |

### Example: POST /notes

**Request Body:**
```json
{
    "title": "My First Note",
    "content": "This is a test of my new Flask API!"
}


{
    "id": "654bafb12345abcdef12345",
    "message": "Note created"
}

