# main.py
from fastapi import FastAPI, Depends, HTTPException
from schemas import Query, Answer
from chains import get_chain
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# To allow cross-origin requests from the frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Educational Q&A Assistant API is running"}

@app.post("/query", response_model=Answer)
async def handle_query(query: Query):
    try:
        chain = get_chain(course_id=query.course_id)
        result = chain(query.question)
        answer_text = result['result']
        return Answer(answer=answer_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
