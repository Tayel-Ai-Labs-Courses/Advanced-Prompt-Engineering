"""
The NLP engine: turns a raw sentence into (intent, entities).

This is keyword + regex matching, not machine learning. That is a deliberate
choice for a first chatbot: every decision it makes is readable in this file,
so when it answers wrong you can see exactly why. A real product would swap
this module for a trained classifier (or Dialogflow/Rasa) and keep the rest
of the system unchanged -- that is the point of keeping it in one file.

Input may be Arabic, English, or Franco-Arabic, because that is how people
actually type in Egypt.
"""

import re
import unicodedata

# ---------------------------------------------------------------- normalizing

ARABIC_DIACRITICS = re.compile(r"[ؗ-ًؚ-ْـ]")

ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def normalize(text):
    """Make spelling variants collapse onto one form before matching.

    'بِيتزَا' , 'بيتزا' and 'بيتزه' all have to look the same to the matcher,
    otherwise every keyword list needs a dozen entries.
    """
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(ARABIC_DIGITS)
    text = ARABIC_DIACRITICS.sub("", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"ؤ", "و", text)
    text = re.sub(r"ئ", "ي", text)
    text = re.sub(r"ة", "ه", text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ------------------------------------------------------------------- intents

# intent -> keywords. Longer/more specific lists are checked by score, so an
# overlapping word ("عايز") does not hijack a clearer one ("المنيو").
INTENT_KEYWORDS = {
    "greet": [
        "السلام عليكم", "سلام عليكم", "صباح الخير", "مساء الخير", "اهلا",
        "هاي", "هلا", "ازيك", "hi", "hello", "hey", "salam", "ezayak",
    ],
    "check_menu": [
        "منيو", "المنيو", "قائمه", "الاصناف", "عندكم ايه", "في ايه",
        "الاسعار", "السعر", "بكام", "كام", "menu", "price", "prices", "list",
    ],
    "order_pizza": [
        "اطلب", "عايز", "عاوز", "محتاج", "هاخد", "هاخذ", "ابغى", "ممكن",
        "بيتزا", "اوردر", "طلب", "order", "want", "pizza", "get me", "3ayz",
        "3awz", "3ayez",
    ],
    "track_order": [
        "اتتبع", "تتبع", "فين طلبي", "طلبي فين", "حاله الطلب", "وصل",
        "الاوردر فين", "track", "where is my order", "status",
    ],
    "affirm": [
        "تمام", "ايوه", "ايوا", "اه", "اوك", "ماشي", "اكيد", "موافق",
        "اكد", "اكدلي", "yes", "yep", "ok", "okay", "sure", "confirm", "aywa",
    ],
    "deny": [
        "لا", "لاء", "مش عايز", "كفايه", "بس كده", "مفيش", "خلاص كده",
        "no", "nope", "nothing", "none", "la",
    ],
    "cancel": [
        "الغي", "الغاء", "كنسل", "بطل", "ابدا من الاول", "من الاول",
        "cancel", "reset", "start over",
    ],
    "thanks": [
        "شكرا", "متشكر", "تسلم", "thanks", "thank you", "thx",
    ],
    "goodbye": [
        "باي", "مع السلامه", "سلام", "bye", "goodbye", "see you",
    ],
    "help": [
        "ساعدني", "مساعده", "بتعمل ايه", "ازاي", "help", "what can you do",
    ],
}

# Intents that should win a tie, because they are the specific request and the
# others are usually just polite filler around them.
INTENT_PRIORITY = [
    "cancel", "track_order", "check_menu", "order_pizza",
    "help", "affirm", "deny", "thanks", "goodbye", "greet",
]


def detect_intent(text):
    """Return (intent_name, confidence 0..1).

    Scoring: each matched keyword is worth its length, so a long specific
    phrase ("فين طلبي") outweighs a short generic one ("لا") that happens to
    appear inside it.
    """
    norm = normalize(text)
    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if _contains_word(norm, kw):
                score += len(kw)
        if score:
            scores[intent] = score

    if not scores:
        return "fallback", 0.0

    best = max(scores.values())
    winners = [i for i, s in scores.items() if s == best]
    if len(winners) > 1:
        winners.sort(key=lambda i: INTENT_PRIORITY.index(i))
    intent = winners[0]
    confidence = min(1.0, best / 12)
    return intent, round(confidence, 2)


def _contains_word(haystack, needle):
    """Substring match, but not in the middle of a longer Latin word.

    Without this, 'no' matches inside 'now' and 'la' inside 'large'.
    Arabic has no such problem here, so it falls back to plain containment.
    """
    if re.fullmatch(r"[a-z0-9 ']+", needle):
        return re.search(r"(?<![a-z])" + re.escape(needle) + r"(?![a-z])", haystack) is not None
    return needle in haystack


# ------------------------------------------------------------------ entities

PIZZA_PATTERNS = {
    "margherita": ["مارجريتا", "مارغريتا", "مرجريتا", "margherita", "margarita"],
    "pepperoni": ["بيبروني", "ببروني", "بيبيروني", "pepperoni", "peperoni"],
    "chicken_ranch": ["تشيكن رانش", "شيكن رانش", "رانش", "chicken ranch", "ranch"],
    "veggie": ["خضار", "خضروات", "نباتي", "veggie", "vegetarian", "vegetable"],
    "four_cheese": ["اربع اجبان", "4 اجبان", "اربعه اجبان", "فور تشيز", "four cheese", "4 cheese"],
    "bbq_chicken": ["باربكيو", "بي بي كيو", "فراخ باربكيو", "bbq", "barbecue"],
}

SIZE_PATTERNS = {
    "small": ["صغير", "صغيره", "سمول", "small", "sghayar"],
    "medium": ["وسط", "متوسط", "متوسطه", "ميديم", "medium", "wasat"],
    "large": ["كبير", "كبيره", "لارج", "large", "big", "kebir", "kbir"],
}

EXTRA_PATTERNS = {
    "extra_cheese": ["جبنه زياده", "جبنه اكسترا", "extra cheese", "اكسترا تشيز"],
    "olives": ["زيتون", "olives", "olive"],
    "mushroom": ["مشروم", "عيش الغراب", "mushroom", "mushrooms"],
    "jalapeno": ["هالابينو", "فلفل حار", "jalapeno", "jalapenos"],
    "corn": ["ذره", "دره", "corn"],
}

NUMBER_WORDS = {
    "واحده": 1, "واحد": 1, "وحده": 1, "اتنين": 2, "اثنين": 2, "تلاته": 3,
    "ثلاثه": 3, "تلات": 3, "اربعه": 4, "اربع": 4, "خمسه": 5, "خمس": 5,
    "سته": 6, "ست": 6, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6,
}

ORDER_ID_RE = re.compile(r"\bpz[-\s]?(\d{4})\b", re.IGNORECASE)
PHONE_RE = re.compile(r"\b(01[0-2,5]\d{8})\b")


def extract_entities(text):
    """Pull every structured value we can find out of one sentence.

    Returns only the keys it is confident about -- a missing key means
    'not mentioned', which is what the dialog manager asks about later.
    """
    norm = normalize(text)
    entities = {}

    # Extras are matched first and then cut out of the sentence. Otherwise
    # "جبنة زيادة" (an extra) would also match the Four Cheese pizza, and the
    # customer's actual flavour choice would be silently overwritten.
    found_extras = []
    remaining = norm
    for key, patterns in EXTRA_PATTERNS.items():
        for p in patterns:
            if _contains_word(remaining, p):
                found_extras.append(key)
                remaining = remaining.replace(p, " ")
                break
    if found_extras:
        entities["extras"] = found_extras

    # Same trick again for the flavour and the size: cut each match out, so
    # the number inside a name ("اربع اجبان", "4 cheese") is not later read
    # as the quantity.
    for key, patterns in PIZZA_PATTERNS.items():
        hit = next((p for p in patterns if _contains_word(remaining, p)), None)
        if hit:
            entities["pizza_type"] = key
            remaining = remaining.replace(hit, " ")
            break

    for key, patterns in SIZE_PATTERNS.items():
        hit = next((p for p in patterns if _contains_word(remaining, p)), None)
        if hit:
            entities["size"] = key
            remaining = remaining.replace(hit, " ")
            break

    quantity = _extract_quantity(remaining)
    if quantity:
        entities["quantity"] = quantity

    phone = PHONE_RE.search(norm)
    if phone:
        entities["phone"] = phone.group(1)

    order_id = ORDER_ID_RE.search(norm)
    if order_id:
        entities["order_id"] = "PZ-" + order_id.group(1)

    return entities


def _extract_quantity(norm):
    """A bare number means quantity -- unless it is a phone number or an id."""
    without_phones = PHONE_RE.sub(" ", ORDER_ID_RE.sub(" ", norm))
    digits = re.findall(r"\b(\d{1,2})\b", without_phones)
    for d in digits:
        value = int(d)
        if 1 <= value <= 20:
            return value
    for word, value in NUMBER_WORDS.items():
        if _contains_word(without_phones, word):
            return value
    return None
