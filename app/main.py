from fastapi import FastAPI
from app.core.db import Base, engine

# from app.features.items.models import Item
from app.features.items.router import router as items_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Vertical Slice (Repo + Service)")
app.include_router(items_router)
