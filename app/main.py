from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.api import routes
from app.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Startup DB init (sync)
        with engine.begin() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            Base.metadata.create_all(bind=conn)
        print("Database initialized >>>>")
    except Exception as e:
        print("Database startup failed: >>>>>", e)
        raise
    yield
    print("App shutdown >>>>")


app = FastAPI(
    title="CareConnect RAG Service",
    lifespan=lifespan
)

app.include_router(routes.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
