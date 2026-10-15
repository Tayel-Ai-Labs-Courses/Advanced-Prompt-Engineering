"""
The dialog manager.

The NLP engine understands one sentence at a time. This module is what makes
it a conversation: it remembers what the customer already said, works out
what is still missing, and asks for exactly that -- one question at a time.

That pattern is called slot filling. The slots are the facts we need before
the kitchen can start, and the bot refuses to move on until they are full.
"""

import re

import menu
import nlp
import store

# The order the bot asks in. Changing this list changes the whole flow, which
# is why the flow lives in data rather than in a chain of if-statements.
SLOT_ORDER = ["pizza_type", "size", "quantity", "extras", "address", "phone"]

QUICK_REPLIES = {
    "pizza_type": [menu.PIZZAS[k]["ar"] for k in menu.PIZZAS],
    "size": ["صغير", "وسط", "كبير"],
    "quantity": ["1", "2", "3"],
    "extras": [menu.EXTRAS[k]["ar"] for k in menu.EXTRAS] + ["بدون إضافات"],
}

QUESTIONS = {
    "pizza_type": "تحب أي نوع بيتزا؟ 🍕",
    "size": "والحجم؟ (صغير / وسط / كبير)",
    "quantity": "عايز كام واحدة؟",
    "extras": "تحب تضيف حاجة؟ (جبنة زيادة، زيتون، مشروم، هالابينو، ذرة) — أو قول «بدون إضافات»",
    "address": "تمام. إيه عنوان التوصيل بالتفصيل؟ 📍",
    "phone": "وآخر حاجة، رقم موبايل للتواصل؟ 📱",
}


def new_session():
    """A fresh conversation. One of these per customer."""
    return {"stage": "idle", "slots": {}, "pending": None}


def greeting():
    return {
        "text": (
            "أهلاً بيك في بيتزا بلانيت 🍕\n"
            "أنا مساعدك الآلي. أقدر أعرضلك المنيو، آخد طلبك، أو أتابع طلب قديم.\n"
            "تحب نبدأ بإيه؟"
        ),
        "chips": ["أشوف المنيو", "عايز أطلب بيتزا", "فين طلبي؟"],
        "debug": {"intent": "greet", "confidence": 1.0, "entities": {}, "slots": {}, "stage": "idle"},
    }


def handle(session, text):
    """One turn of the conversation: customer text in, bot reply out."""
    intent, confidence = nlp.detect_intent(text)
    entities = nlp.extract_entities(text)

    # --- context beats keywords -------------------------------------------
    # The same word means different things depending on what we just asked.
    # "لا" after "any extras?" is an answer; "لا" out of nowhere is not.
    intent = _apply_context(session, text, intent, entities)

    reply = _route(session, text, intent, entities)

    reply["debug"] = {
        "intent": intent,
        "confidence": confidence,
        "entities": entities,
        "slots": dict(session["slots"]),
        "stage": session["stage"],
        "pending": session["pending"],
    }
    return reply


def _apply_context(session, text, intent, entities):
    """Re-read the intent in light of the question the bot just asked."""
    norm = nlp.normalize(text)
    pending = session["pending"]

    # A free-text answer to "what is your address?" must never be classified.
    # "عايز" inside an address would otherwise restart the order.
    if pending == "address" and len(norm) >= 5 and intent not in ("cancel",):
        return "provide_address"

    if pending == "extras" and intent in ("deny", "thanks", "fallback"):
        if any(nlp._contains_word(norm, k) for k in
               ("بدون", "مفيش", "لا", "كفايه", "بس كده", "no", "none", "nothing")):
            return "deny"

    if session["stage"] == "confirming":
        # At the summary there are only two meaningful answers: yes or no.
        # Check the words directly instead of trusting the winning intent --
        # "أكد الطلب" contains "طلب" and would otherwise score as a brand new
        # order and loop the customer back to the summary forever.
        if intent in ("deny", "cancel"):
            return "cancel"
        if intent == "thanks" or any(
            nlp._contains_word(norm, k) for k in nlp.INTENT_KEYWORDS["affirm"]
        ):
            return "affirm"

    # Bare entity with no clear intent, mid-order: it is an answer to the
    # pending question, not a new topic.
    if intent == "fallback" and entities and session["stage"] == "filling":
        return "provide_info"

    return intent


def _route(session, text, intent, entities):
    """Pick the handler for this intent."""
    if intent == "cancel":
        session.update(new_session())
        return {
            "text": "تم إلغاء الطلب. لو حبيت تبدأ من جديد أنا موجود 👍",
            "chips": ["عايز أطلب بيتزا", "أشوف المنيو"],
        }

    if intent == "check_menu":
        reply = {"text": menu.menu_text(), "chips": ["عايز أطلب بيتزا"]}
        # Do not lose our place: if we were mid-order, repeat the question.
        if session["stage"] == "filling" and session["pending"]:
            reply["text"] += "\n\n" + QUESTIONS[session["pending"]]
            reply["chips"] = QUICK_REPLIES.get(session["pending"], [])
        return reply

    if intent == "track_order":
        return _track(entities)

    if intent == "help":
        return {
            "text": (
                "أقدر أساعدك في:\n"
                "• عرض المنيو والأسعار\n"
                "• طلب بيتزا من أول النوع لحد التوصيل\n"
                "• تتبع طلب برقمه (مثلاً PZ-1001)\n"
                "اكتب اللي عايزه بالعربي أو بالإنجليزي."
            ),
            "chips": ["أشوف المنيو", "عايز أطلب بيتزا"],
        }

    if intent == "greet":
        return greeting()

    if intent == "goodbye":
        return {"text": "سلام! استنيك تاني 🍕", "chips": []}

    if intent == "affirm" and session["stage"] == "confirming":
        return _place_order(session)

    if intent == "provide_address":
        session["slots"]["address"] = text.strip()
        return _advance(session)

    if intent == "deny" and session["pending"] == "extras":
        session["slots"]["extras"] = []
        return _advance(session)

    if intent in ("order_pizza", "provide_info", "affirm"):
        return _fill_from(session, entities, text)

    if intent == "thanks":
        return {"text": "تحت أمرك 🙏", "chips": []}

    # fallback: we genuinely did not understand
    if session["stage"] == "confirming":
        # Never drop a finished order because of one unclear message --
        # show the summary again and keep waiting for yes or no.
        return {
            "text": "معلش مفهمتش 🤔 تحب أأكد الطلب ولا ألغيه؟\n\n" + _summary(session["slots"]),
            "chips": ["أكد الطلب ✅", "إلغاء"],
        }

    if session["stage"] == "filling" and session["pending"]:
        return {
            "text": "معلش مفهمتش 🤔 " + QUESTIONS[session["pending"]],
            "chips": QUICK_REPLIES.get(session["pending"], []),
        }
    return {
        "text": (
            "معلش، مفهمتش قصدك. أقدر أعرضلك المنيو، أو آخد طلبك، "
            "أو أتابع طلب برقمه."
        ),
        "chips": ["أشوف المنيو", "عايز أطلب بيتزا", "فين طلبي؟"],
    }


NO_EXTRAS_PHRASES = ("بدون اضافات", "من غير اضافات", "بدون", "no extras", "plain")


def _fill_from(session, entities, text=""):
    """Write whatever the customer just told us into the slots."""
    session["stage"] = "filling"
    slots = session["slots"]

    # "مارجريتا كبيرة بدون إضافات" answers the extras question before it is
    # asked. Without this the bot would ask anyway, which feels robotic.
    norm = nlp.normalize(text)
    if any(nlp._contains_word(norm, p) for p in NO_EXTRAS_PHRASES):
        slots.setdefault("extras", [])

    for key in ("pizza_type", "size", "quantity"):
        if key in entities:
            slots[key] = entities[key]

    if "extras" in entities:
        # Merge, so "and olives too" adds instead of replacing.
        slots["extras"] = sorted(set(slots.get("extras", [])) | set(entities["extras"]))

    if "phone" in entities:
        slots["phone"] = entities["phone"]

    return _advance(session)


def _advance(session):
    """The engine of the flow: ask for the first slot that is still empty."""
    slots = session["slots"]
    for slot in SLOT_ORDER:
        if slot not in slots:
            session["pending"] = slot
            session["stage"] = "filling"
            return {"text": QUESTIONS[slot], "chips": QUICK_REPLIES.get(slot, [])}

    if "address" not in slots:
        session["pending"] = "address"
        return {"text": QUESTIONS["address"], "chips": []}

    # Everything is full -> show the summary and wait for a yes.
    session["pending"] = None
    session["stage"] = "confirming"
    return {"text": _summary(slots), "chips": ["أكد الطلب ✅", "إلغاء"]}


def _summary(slots):
    pizza = menu.PIZZAS[slots["pizza_type"]]
    size = menu.SIZES[slots["size"]]
    qty = slots["quantity"]
    extras = slots.get("extras", [])
    unit = menu.price_of(slots["pizza_type"], slots["size"])
    extras_cost = menu.extras_total(extras)
    total = menu.order_total(slots["pizza_type"], slots["size"], qty, extras)

    lines = [
        "📋 ملخص طلبك:",
        f"• {pizza['ar']} — حجم {size['ar']} × {qty}",
        f"• الإضافات: " + ("، ".join(menu.EXTRAS[e]["ar"] for e in extras) if extras else "بدون"),
        f"• العنوان: {slots['address']}",
        f"• الموبايل: {slots['phone']}",
        "",
        f"سعر الواحدة: {unit} ج"
        + (f" + إضافات {extras_cost} ج" if extras_cost else ""),
        f"التوصيل: {menu.DELIVERY_FEE} ج",
        f"💰 الإجمالي: {total} {menu.CURRENCY}",
        "",
        "أأكد الطلب؟",
    ]
    return "\n".join(lines)


def _place_order(session):
    slots = session["slots"]
    total = menu.order_total(
        slots["pizza_type"], slots["size"], slots["quantity"], slots.get("extras", [])
    )
    order_id = store.create_order(slots, total)
    session.update(new_session())
    return {
        "text": (
            f"تم تأكيد طلبك 🎉\n"
            f"رقم الطلب: {order_id}\n"
            f"الإجمالي: {total} {menu.CURRENCY}\n"
            f"الوقت المتوقع: 30-40 دقيقة 🛵\n\n"
            f"احفظ الرقم لو حبيت تتابع الطلب."
        ),
        "chips": [f"فين طلبي {order_id}"],
    }


def _track(entities):
    order_id = entities.get("order_id")
    if not order_id:
        return {
            "text": "ابعتلي رقم الطلب وأنا أقولك وصل فين (الشكل كده: PZ-1001)",
            "chips": [],
        }
    order = store.get_order(order_id)
    if not order:
        return {"text": f"ملقيتش طلب بالرقم {order_id} 🤔 تأكد من الرقم.", "chips": []}
    pizza = menu.PIZZAS[order["pizza_type"]]["ar"]
    size = menu.SIZES[order["size"]]["ar"]
    return {
        "text": (
            f"طلب {order['id']}\n"
            f"{pizza} — {size} × {order['quantity']}\n"
            f"الإجمالي: {order['total']} {menu.CURRENCY}\n"
            f"الحالة: {store.STATUS_FLOW[order['status']]}"
        ),
        "chips": [],
    }
