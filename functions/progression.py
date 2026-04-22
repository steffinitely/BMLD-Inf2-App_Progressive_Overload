# functions/progression.py

def calculate_progression(last_weight):
    """
    Erhöht das Gewicht um 2.5%
    """
    if last_weight is None:
        return None

    new_weight = last_weight * 1.025

    return new_weight


def calculate_training_volume(weight, reps, sets):
    """
    Berechnet Trainingsvolumen
    """
    return weight * reps * sets


def get_last_entry(workout_list):
    """
    Gibt den letzten Eintrag zurück
    """
    if workout_list:
        return workout_list[-1]
    return None