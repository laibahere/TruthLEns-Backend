from fastapi import FastAPI, File, UploadFile
import shutil
from auth import router as auth_router
from your_notebook import analyze_image  # Import the function from your converted notebook

app = FastAPI()  # Define the FastAPI app

# Include authentication routes
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def home():
    return {"message": "Backend is running!"}

# Image Upload and Analysis Route
@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run your model's function
    result = analyze_image(file_path)

    return {"result": result}
