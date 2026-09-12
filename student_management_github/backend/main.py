import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Set SUPABASE_URL and SUPABASE_KEY environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Student Management System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Student(BaseModel):
    name: str
    course: str
    marks: int


class MarksUpdate(BaseModel):
    marks: int


@app.get("/")
def home():
    return {"message": "Student Management System API is running"}


@app.get("/students")
def get_students():
    response = supabase.table("students").select("*").order("id").execute()
    return response.data


@app.get("/students/{student_id}")
def get_student(student_id: int):
    response = supabase.table("students").select("*").eq("id", student_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Student not found")
    return response.data[0]


@app.post("/students")
def create_student(student: Student):
    if not student.name.strip() or not student.course.strip():
        raise HTTPException(status_code=400, detail="Name and course are required")
    if student.marks < 0 or student.marks > 100:
        raise HTTPException(status_code=400, detail="Marks must be between 0 and 100")

    response = supabase.table("students").insert({
        "name": student.name.strip(),
        "course": student.course.strip(),
        "marks": student.marks
    }).execute()

    return {"message": "Student created successfully", "data": response.data}


@app.put("/students/{student_id}")
def update_student(student_id: int, student: MarksUpdate):
    if student.marks < 0 or student.marks > 100:
        raise HTTPException(status_code=400, detail="Marks must be between 0 and 100")

    response = (
        supabase.table("students")
        .update({"marks": student.marks})
        .eq("id", student_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student updated successfully", "data": response.data}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    response = supabase.table("students").delete().eq("id", student_id).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully", "data": response.data}
