from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
import os
from typing import List, Optional

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Use absolute path to the CSV file
CSV_FILE = os.path.join(os.path.dirname(__file__), "q-fastapi.csv")

def read_students():
    students = []
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append({
                "studentId": int(row["studentId"]),
                "class": row["class"]
            })
    return students

@app.get("/api")
def get_students(class_filter: Optional[List[str]] = Query(None, alias="class")):
    all_students = read_students()
    if class_filter:
        filtered_students = [s for s in all_students if s["class"] in class_filter]
        return {"students": filtered_students}
    return {"students": all_students}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
