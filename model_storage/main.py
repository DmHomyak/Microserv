from fastapi import FastAPI, HTTPException
from models.model import BlendModel
from database.db import SessionDep
from database.db import wait_for_db
from sqlmodel import select
import requests


app = FastAPI()

@app.on_event("startup")
def on_startup():
    wait_for_db()

@app.post("/models/")
async def add_model(
    id: int, name: str, vertices: int, edges: int, faces: int, render_time: float, is_ready: bool, session: SessionDep):
    blend = BlendModel(id=id, name=name, vertices=vertices, edges=edges, faces=faces, render_time=render_time,
                       is_ready=is_ready)
    session.add(blend)
    session.commit()
    session.refresh(blend)

@app.get("/models")
async def model_info(session: SessionDep):
    model = session.exec(select(BlendModel)).all()
    return model
