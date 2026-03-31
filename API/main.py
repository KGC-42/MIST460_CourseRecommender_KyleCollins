from fastapi import FastAPI
from routes import router

app = FastAPI(title="MIST 460 Course Recommender API - Kyle Collins")

app.include_router(router, prefix="/api", tags=["courses"])

@app.get("/")
def read_root():
    return {"message": "MIST 460 Course Recommender API", "student": "Kyle Collins"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)