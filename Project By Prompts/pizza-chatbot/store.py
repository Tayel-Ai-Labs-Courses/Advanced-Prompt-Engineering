"""
The database layer.

A JSON file on disk, which is enough to prove the concept: orders survive a
server restart and can be looked up by id. Swapping this for PostgreSQL or a
call to the restaurant's API means rewriting these four functions and nothing
else -- the dialog manager never touches the file directly.
"""

import json
import os
from datetime import datetime

ORDERS_FILE = os.path.join(os.path.dirname(__file__), "orders.json")

# The lifecycle an order moves through in the kitchen.
STATUS_FLOW = {
    "received": "تم استلام طلبك ✅",
    "preparing": "بنحضّر البيتزا في الفرن 👨‍🍳",
    "on_the_way": "الطلب في الطريق إليك 🛵",
    "delivered": "تم التوصيل، بالهنا والشفا 🎉",
}


def _load():
    if not os.path.exists(ORDERS_FILE):
        return {"last_id": 1000, "orders": {}}
    with open(ORDERS_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_order(slots, total):
    """Persist a completed order and return its new id."""
    data = _load()
    data["last_id"] += 1
    order_id = f"PZ-{data['last_id']}"
    data["orders"][order_id] = {
        "id": order_id,
        "pizza_type": slots["pizza_type"],
        "size": slots["size"],
        "quantity": slots["quantity"],
        "extras": slots.get("extras", []),
        "address": slots["address"],
        "phone": slots["phone"],
        "total": total,
        "status": "received",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    _save(data)
    return order_id


def get_order(order_id):
    return _load()["orders"].get(order_id.upper())


def set_status(order_id, status):
    """Used by the kitchen, not by the bot. Here so tracking has something
    to report other than 'received' forever."""
    data = _load()
    order = data["orders"].get(order_id.upper())
    if not order:
        return False
    order["status"] = status
    _save(data)
    return True
