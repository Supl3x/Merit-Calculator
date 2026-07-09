# ── Merit Calculator — Constants & Configuration ─────────────────────────────
# Centralised place for seat capacities, display names, colour palettes, etc.

SPECIALIZATIONS = {
    "Computer Science - (No Specialisation)": {
        "code": "CS",
        "seats": 100,
        "color": "#6C63FF",           # Indigo-violet
        "gradient": "linear-gradient(135deg, #6C63FF, #3B82F6)",
        "emoji": "💻",
    },
    "Data Science": {
        "code": "DS",
        "seats": 50,
        "color": "#10B981",           # Emerald
        "gradient": "linear-gradient(135deg, #10B981, #06D6A0)",
        "emoji": "📊",
    },
    "Artificial Intelligence": {
        "code": "AI",
        "seats": 50,
        "color": "#F59E0B",           # Amber
        "gradient": "linear-gradient(135deg, #F59E0B, #F97316)",
        "emoji": "🤖",
    },
    "Cyber Security": {
        "code": "CY",
        "seats": 50,
        "color": "#EF4444",           # Rose-red
        "gradient": "linear-gradient(135deg, #EF4444, #EC4899)",
        "emoji": "🔒",
    },
    "Gaming & Animation": {
        "code": "GA",
        "seats": 50,
        "color": "#8B5CF6",           # Purple
        "gradient": "linear-gradient(135deg, #8B5CF6, #D946EF)",
        "emoji": "🎮",
    },
}

# Quick-lookup helpers
CODE_TO_NAME = {v["code"]: k for k, v in SPECIALIZATIONS.items()}
NAME_TO_CODE = {k: v["code"] for k, v in SPECIALIZATIONS.items()}

TOTAL_SEATS = sum(v["seats"] for v in SPECIALIZATIONS.values())  # 300

CHOICE_COLUMNS = ["choice_1", "choice_2", "choice_3", "choice_4", "choice_5"]

# Plotly / chart colour sequence (same order as SPECIALIZATIONS)
COLOR_SEQUENCE = [v["color"] for v in SPECIALIZATIONS.values()]

NO_RESPONSE = "No response submitted"
