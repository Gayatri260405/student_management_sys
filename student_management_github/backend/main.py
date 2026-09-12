import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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
# API STATUS
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

    try:
        response = (
            supabase
            .table("students")
            .select("*")
            .order("id")
            .execute()
        )

        return response.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch students: {str(e)}"
        )


# =========================================================
# GET ONE STUDENT
# =========================================================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    try:
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

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch student: {str(e)}"
        )


# =========================================================
# CREATE STUDENT
# =========================================================

@app.post("/students")
def create_student(student: Student):

    if not student.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Name is required"
        )

    if not student.course.strip():
        raise HTTPException(
            status_code=400,
            detail="Course is required"
        )

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

    try:
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create student: {str(e)}"
        )


# =========================================================
# UPDATE STUDENT MARKS
# =========================================================

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: MarksUpdate
):

    if student.marks < 0 or student.marks > 100:
        raise HTTPException(
            status_code=400,
            detail="Marks must be between 0 and 100"
        )

    try:
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

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update student: {str(e)}"
        )


# =========================================================
# DELETE STUDENT
# =========================================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    try:
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

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete student: {str(e)}"
        )


# =========================================================
# FRONTEND
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# Check that frontend folder exists
if not FRONTEND_DIR.exists():
    raise RuntimeError(
        f"Frontend folder not found: {FRONTEND_DIR}"
    )


# Serve CSS, JavaScript and other frontend files
app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)


# Serve index.html at /
@app.get("/")
def serve_frontend():
    return FileResponse(
        str(FRONTEND_DIR / "index.html")
    )
