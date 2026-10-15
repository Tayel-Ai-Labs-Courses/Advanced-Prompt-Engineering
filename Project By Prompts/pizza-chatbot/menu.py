"""
The restaurant system.

In a real deployment this would be a database or an API call to the
restaurant's POS. Here it is a plain Python dict so the bot stays runnable
with zero setup. Everything the bot says about prices comes from this file
and nowhere else -- so changing a price here changes it everywhere.
"""

CURRENCY = "EGP"
DELIVERY_FEE = 20

SIZES = {
    "small": {"ar": "صغير", "en": "Small"},
    "medium": {"ar": "وسط", "en": "Medium"},
    "large": {"ar": "كبير", "en": "Large"},
}

# key -> display names + price per size
PIZZAS = {
    "margherita": {
        "ar": "مارجريتا",
        "en": "Margherita",
        "prices": {"small": 90, "medium": 130, "large": 170},
    },
    "pepperoni": {
        "ar": "بيبروني",
        "en": "Pepperoni",
        "prices": {"small": 110, "medium": 150, "large": 200},
    },
    "chicken_ranch": {
        "ar": "تشيكن رانش",
        "en": "Chicken Ranch",
        "prices": {"small": 120, "medium": 165, "large": 215},
    },
    "veggie": {
        "ar": "خضار",
        "en": "Veggie",
        "prices": {"small": 95, "medium": 135, "large": 175},
    },
    "four_cheese": {
        "ar": "أربع أجبان",
        "en": "Four Cheese",
        "prices": {"small": 125, "medium": 170, "large": 220},
    },
    "bbq_chicken": {
        "ar": "باربكيو تشيكن",
        "en": "BBQ Chicken",
        "prices": {"small": 120, "medium": 165, "large": 215},
    },
}

EXTRAS = {
    "extra_cheese": {"ar": "جبنة زيادة", "en": "Extra cheese", "price": 20},
    "olives": {"ar": "زيتون", "en": "Olives", "price": 10},
    "mushroom": {"ar": "مشروم", "en": "Mushroom", "price": 15},
    "jalapeno": {"ar": "هالابينو", "en": "Jalapeno", "price": 10},
    "corn": {"ar": "ذرة", "en": "Corn", "price": 10},
}


def price_of(pizza_key, size_key):
    return PIZZAS[pizza_key]["prices"][size_key]


def extras_total(extra_keys):
    return sum(EXTRAS[k]["price"] for k in extra_keys)


def order_total(pizza_key, size_key, quantity, extra_keys):
    """Total for the whole order, delivery included."""
    per_pizza = price_of(pizza_key, size_key) + extras_total(extra_keys)
    return per_pizza * quantity + DELIVERY_FEE


def menu_text():
    """The menu as a chat message."""
    lines = ["🍕 منيو البيتزا (الأسعار بالجنيه):", ""]
    for p in PIZZAS.values():
        prices = p["prices"]
        lines.append(
            f"• {p['ar']} ({p['en']}) — "
            f"صغير {prices['small']} / وسط {prices['medium']} / كبير {prices['large']}"
        )
    lines.append("")
    lines.append("الإضافات: " + "، ".join(
        f"{e['ar']} +{e['price']}" for e in EXTRAS.values()
    ))
    lines.append(f"التوصيل: {DELIVERY_FEE} جنيه")
    return "\n".join(lines)
