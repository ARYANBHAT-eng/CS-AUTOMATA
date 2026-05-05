from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI Customer Success Automation System is running 🚀"}