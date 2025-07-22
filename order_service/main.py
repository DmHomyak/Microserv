from fastapi import FastAPI, HTTPException
from models.order import Order
from database.db import wait_for_db
from database.db import SessionDep
import requests
from sqlmodel import select


app = FastAPI()


@app.on_event("startup")
def on_startup():
    wait_for_db()


@app.get("/order_service/order/{title}")
async def order_info(title: str, session: SessionDep):
    orders = session.exec(select(Order).where(Order.title == title)).all()
    return orders


@app.post("/order_service/order/{title}")
async def add_order(id: int, title: str, price: int, deadline: str, session: SessionDep):
    order = Order(id=id, title=title, price=price, deadline=deadline)
    session.add(order)
    session.commit()
    session.refresh(order)


@app.get("/order_service/check_model/{model_name}")
def check_model_ready(model_name: str):
    try:
        response = requests.get(f"http://model_storage:8000/models")
        response.raise_for_status()
        models = response.json()

        matched = next((m for m in models if m.get("name") == model_name), None)
        if not matched:
            return {"model_name": model_name, "found": False, "is_ready": False}
        return {
            "model_name": model_name,
            "found": True,
            "is_ready": matched.get("is_ready", False)
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error contacting model storage: {e}")