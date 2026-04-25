# functions/progression.py

import pandas as pd


# =========================
# 🔹 BASIC CALCULATIONS
# =========================

def calculate_training_volume(weight, reps, sets):
    """
    Trainingsvolumen = Gewicht × Wiederholungen × Sätze
    """
    if weight is None or reps is None or sets is None:
        return 0
    return weight * reps * sets


def estimate_1rm(weight, reps):
    """
    Schätzt das 1RM (Epley-Formel)
    """
    if weight is None or reps is None or reps == 0:
        return 0
    return weight * (1 + reps / 30)


def round_weight(weight):
    """
    Rundet auf 0.5 kg (Standard im Gym)
    """
    return round(weight * 2) / 2


# =========================
# 🔹 HELPER FUNCTIONS
# =========================

def get_last_entries(exercise_data, n=2):
    """
    Holt die letzten n Einträge einer Übung
    """
    if exercise_data is None or exercise_data.empty:
        return []

    return exercise_data.sort_values("timestamp").tail(n).to_dict("records")


def normalize_difficulty(difficulty):
    """
    Wandelt Difficulty in Score um
    """
    mapping = {
        "Sehr einfach": 1,
        "Einfach": 2,
        "Gut": 3,
        "Schwierig": 4,
        "Sehr schwierig": 5
    }
    return mapping.get(difficulty, 3)


# =========================
# 🔹 PROGRESSION ENGINE
# =========================

def get_suggested_weight(
    exercise_name,
    data_df,
    rep_range=(8, 12)
):
    """
    Intelligente Progression basierend auf:
    - Reps
    - Gewicht
    - Difficulty
    - Volumen
    - 1RM Entwicklung

    Returns:
        dict:
        {
            "weight": float,
            "action": str,
            "reason": str,
            "estimated_1rm": float
        }
    """

    # 🔹 Keine Daten vorhanden
    if data_df is None or data_df.empty:
        return {
            "weight": 0.0,
            "action": "start",
            "reason": "no data",
            "estimated_1rm": 0
        }

    # 🔹 Übung filtern
    exercise_data = data_df[
        data_df['exercise'].str.lower() == exercise_name.lower()
    ]

    if exercise_data.empty:
        return {
            "weight": 0.0,
            "action": "start",
            "reason": "no exercise history",
            "estimated_1rm": 0
        }

    entries = get_last_entries(exercise_data, 2)

    # 🔹 Nur ein Eintrag → einfach wiederholen
    if len(entries) == 1:
        last = entries[0]
        return {
            "weight": last["weight"],
            "action": "repeat",
            "reason": "only one entry",
            "estimated_1rm": estimate_1rm(last["weight"], last["reps"])
        }

    last = entries[-1]
    prev = entries[-2]

    weight = last["weight"]
    reps = last["reps"]
    sets = last["sets"]

    prev_weight = prev["weight"]
    prev_reps = prev["reps"]
    prev_sets = prev["sets"]

    min_reps, max_reps = rep_range

    # =========================
    # 🔹 METRICS
    # =========================

    last_volume = calculate_training_volume(weight, reps, sets)
    prev_volume = calculate_training_volume(prev_weight, prev_reps, prev_sets)

    last_1rm = estimate_1rm(weight, reps)
    prev_1rm = estimate_1rm(prev_weight, prev_reps)

    difficulty_score = normalize_difficulty(last.get("difficulty"))

    # =========================
    # 🔹 PROGRESSION LOGIC
    # =========================

    # 🔹 Fortschritt erkannt
    progress_made = (
        reps > prev_reps or
        weight > prev_weight or
        last_volume > prev_volume or
        last_1rm > prev_1rm
    )

    # 🔹 Gewichtserhöhung basierend auf Difficulty
    if difficulty_score <= 2:
        increase_factor = 1.05   # leicht → stärker steigern
    elif difficulty_score == 3:
        increase_factor = 1.025  # normal
    else:
        increase_factor = 1.0    # schwer → nicht steigern

    # =========================
    # 🔹 CASES
    # =========================

    # ✅ Fall 1: obere Rep-Grenze erreicht + Fortschritt
    if reps >= max_reps and progress_made:
        new_weight = round_weight(weight * increase_factor)

        return {
            "weight": new_weight,
            "action": "increase_weight",
            "reason": "max reps reached",
            "estimated_1rm": last_1rm
        }

    # 🔁 Fall 2: innerhalb Range → mehr Reps
    if reps < max_reps and progress_made:
        return {
            "weight": weight,
            "action": "increase_reps",
            "reason": "progress within range",
            "estimated_1rm": last_1rm
        }

    # ⚠️ Fall 3: kein Fortschritt
    if not progress_made:
        return {
            "weight": weight,
            "action": "repeat",
            "reason": "no progress",
            "estimated_1rm": last_1rm
        }

    # 🔻 Fall 4: sehr schwer → Deload optional
    if difficulty_score >= 5:
        new_weight = round_weight(weight * 0.95)

        return {
            "weight": new_weight,
            "action": "deload",
            "reason": "too difficult",
            "estimated_1rm": last_1rm
        }

    # Default
    return {
        "weight": weight,
        "action": "repeat",
        "reason": "default",
        "estimated_1rm": last_1rm
    }