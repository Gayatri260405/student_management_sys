// Change this when your backend is deployed on Render.
const API_URL = "";

async function loadStudents() {
    const table = document.getElementById("studentTable");

    try {
        const response = await fetch(`${API_URL}/students`);

        if (!response.ok) {
            throw new Error("Could not load students");
        }

        const students = await response.json();

        table.innerHTML = "";

        students.forEach(student => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${student.id}</td>
                <td>${escapeHtml(student.name)}</td>
                <td>${escapeHtml(student.course)}</td>
                <td>${student.marks}</td>
                <td>
                    <button class="edit-btn"
                        onclick="updateMarks(${student.id}, ${student.marks})">
                        Edit
                    </button>
                    <button class="delete-btn"
                        onclick="deleteStudent(${student.id})">
                        Delete
                    </button>
                </td>
            `;

            table.appendChild(row);
        });
    } catch (error) {
        showMessage("Backend is not running or URL is incorrect.", true);
        console.error(error);
    }
}

async function addStudent() {
    const name = document.getElementById("name").value.trim();
    const course = document.getElementById("course").value.trim();
    const marks = Number(document.getElementById("marks").value);

    if (!name || !course || Number.isNaN(marks)) {
        showMessage("Please enter name, course and marks.", true);
        return;
    }

    try {
        const response = await fetch(`${API_URL}/students`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name, course, marks})
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Could not add student");
        }

        showMessage("Student added successfully.");
        document.getElementById("name").value = "";
        document.getElementById("course").value = "";
        document.getElementById("marks").value = "";

        loadStudents();
    } catch (error) {
        showMessage(error.message, true);
    }
}

async function updateMarks(id, oldMarks) {
    const newMarks = prompt("Enter new marks (0-100):", oldMarks);

    if (newMarks === null) return;

    const marks = Number(newMarks);

    if (Number.isNaN(marks) || marks < 0 || marks > 100) {
        showMessage("Marks must be between 0 and 100.", true);
        return;
    }

    try {
        const response = await fetch(`${API_URL}/students/${id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({marks})
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Could not update student");
        }

        showMessage("Marks updated successfully.");
        loadStudents();
    } catch (error) {
        showMessage(error.message, true);
    }
}

async function deleteStudent(id) {
    if (!confirm("Are you sure you want to delete this student?")) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/students/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Could not delete student");
        }

        showMessage("Student deleted successfully.");
        loadStudents();
    } catch (error) {
        showMessage(error.message, true);
    }
}

function showMessage(message, error = false) {
    const element = document.getElementById("message");
    element.textContent = message;
    element.style.color = error ? "red" : "green";
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

loadStudents();
