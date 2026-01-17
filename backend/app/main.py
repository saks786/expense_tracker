# backend/app/main.py
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routes import router
from .payments import router as payment_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("expense-backend")

app = FastAPI(title="Expense Tracker API", version="2.0.0")

# CORS - keep narrow in production; allow_origins=["*"] only for temporary testing.
frontend_origins = [
    "http://localhost:5173",
    "http://localhost:5413",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,  # don't duplicate keys
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables at startup — log errors but don't crash the entire process
@app.on_event("startup")
async def on_startup():
    logger.info("Startup: attempting to create/verify DB tables...")
    try:
        models.Base.metadata.create_all(bind=engine)
        logger.info("DB tables created/verified.")
    except Exception as e:
        # Log exception (important); don't re-raise to keep process alive
        logger.exception("Failed to create DB tables on startup — check DATABASE_URL and DB connectivity: %s", e)

# small root + ping endpoints for health checks
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Expense Tracker backend is running"}

@app.get("/ping")
async def ping():
    return {"pong": True}

# include API routers
app.include_router(router)
app.include_router(payment_router)
