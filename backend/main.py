from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, leave_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://husky-assign-jk04ayj2p-skes2712-8232s-projects.vercel.app",
        "https://husky-assign.vercel.app/",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(leave_routes.router)
