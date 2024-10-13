from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend import most_similar_perfumes, get_heatmap
import uvicorn

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:8000",  # อนุญาตที่อยู่ต้นทางนี้
    "http://127.0.0.1:8000",  # อนุญาตที่อยู่ต้นทางนี้
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # อนุญาตวิธีการทั้งหมด
    allow_headers=["*"],  # อนุญาตส่วนหัวทั้งหมด
)

# Input schema for perfume similarity request
class Perfume(BaseModel):
    scents: str
    base_notes: list
    middle_notes: list
    department: str

@app.post("/similar-perfumes")
def similar_perfumes(data: Perfume):
    data.base_notes = ",".join(data.base_notes)
    data.middle_notes= ",".join(data.middle_notes)
    result = most_similar_perfumes(data.scents, data.base_notes, data.middle_notes, data.department)
    
    if result is None:
        return "No perfumes found for the given department"
    return result.to_dict(orient="records")

@app.get("/perfume-correlations/{department}")
def perfume_correlations(department: str):
    heatmap = get_heatmap(department)
    
    if heatmap is None:
        return "No perfumes found for the given department"
    return {"heatmap": heatmap}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
