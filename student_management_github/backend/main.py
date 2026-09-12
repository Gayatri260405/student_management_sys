import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Set SUPABASE_URL and SUPABASE_KEY environment variables."
    )


# =========================================================
# SUPABASE
# =========================================================

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title="Student Management System",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# DATA MODELS
# =========================================================

class Student(BaseModel):
    name: str
    course: str
    marks: int


class MarksUpdate(BaseModel):
    marks: int


# =========================================================
# HOME / API STATUS
# =========================================================

@app.get("/api")
def api_home():
    return {
        "message": "Student Management System API is running"
    }


# =========================================================
# GET ALL STUDENTS
# =========================================================

@app.get("/students")
def get_students():

    response = (
        supabase
        .table("students")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data


# =========================================================
# GET ONE STUDENT
# =========================================================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    response = (
        supabase
        .table("students")
        .select("*")
        .eq("id", student_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return response.data[0]


# =========================================================
# CREATE STUDENT
# =========================================================

@app.post("/students")
def create_student(student: Student):

    # Validate name
    if not student.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Name is required"
        )

    # Validate course
    if not student.course.strip():
        raise HTTPException(
            status_code=400,
            detail="Course is required"
        )

    # Validate marks
    if student.marks < 0 or student.marks > 100:
        raise HTTPException(
            status_code=400,
            detail="Marks must be between 0 and 100"
        )

    student_data = {
        "name": student.name.strip(),
        "course": student.course.strip(),
        "marks": student.marks
    }

    response = (
        supabase
        .table("students")
        .insert(student_data)
        .execute()
    )

    return {
        "message": "Student created successfully",
        "data": response.data
    }


# =========================================================
# UPDATE STUDENT MARKS
# =========================================================

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: MarksUpdate
):

    # Validate marks
    if student.marks < 0 or student.marks > 100:
        raise HTTPException(
            status_code=400,
            detail="Marks must be between 0 and 100"
        )

    response = (
        supabase
        .table("students")
        .update({
            "marks": student.marks
        })
        .eq("id", student_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student updated successfully",
        "data": response.data
    }


# =========================================================
# DELETE STUDENT
# =========================================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    response = (
        supabase
        .table("students")
        .delete()
        .eq("id", student_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully",
        "data": response.data
    }


# =========================================================
# SERVE FRONTEND
# =========================================================

# Project structure:
#
# student_management_github/
# │
# ├── backend/
# │   └── main.py
# │
# ├── frontend/
# │   ├── index.html
# │   ├── style.css
# │   └── script.js
# │
# └── requirements.txt

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Serve HTML, CSS and JavaScript
# This must come AFTER the API routes.
app.mount(
    "/",
    StaticFiles(
        directory=str(FRONTEND_DIR),
        html=True
    ),
    name="frontend"
)
