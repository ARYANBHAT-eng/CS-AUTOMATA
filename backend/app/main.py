from fastapi import FastAPI

from app.routes.activity import router as activity_router
from app.routes.users import router as users_router

app = FastAPI()


app.include_router(users_router)
app.include_router(activity_router)


@app.get("/")
def root():
    return {"message": "CS Automata is running 🚀"}
