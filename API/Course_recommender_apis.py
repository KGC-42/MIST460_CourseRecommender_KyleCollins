from fastapi import FastAPI
from get_course_sections_for_specified_course import router as sections_router
from get_course_prerequisites import router as prerequisites_router

app = FastAPI(title="MIST 460 Course Recommender API - Kyle Collins")

# Include routers
app.include_router(sections_router, prefix="/api", tags=["courses"])
app.include_router(prerequisites_router, prefix="/api", tags=["courses"])

@app.get("/")
def read_root():
    return {"message": "MIST 460 Course Recommender API", "student": "Kyle Collins"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)