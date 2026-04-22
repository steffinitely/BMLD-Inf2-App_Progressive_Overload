# functions/progression.py
import pandas as pd

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


def get_suggested_weight(exercise_name, data_df):
    """
    Berechnet das nächste vorgeschlagene Startgewicht für eine Übung.
    
    Basiert auf dem letzten Gewicht aus der Trainingshistorie und erhöht es um 2.5%.
    
    Args:
        exercise_name (str): Name der Übung (z.B. "Barbell Benchpress")
        data_df (pd.DataFrame): DataFrame mit den Trainingsdaten
    
    Returns:
        float: Das vorgeschlagene Startgewicht (gerundet auf 0.5 kg)
              oder 0.0 wenn keine Historie vorhanden ist
    """
    if data_df is None or data_df.empty:
        return 0.0
    
    # Filtere nach der Übung (case-insensitive)
    exercise_data = data_df[
        data_df['exercise'].str.lower() == exercise_name.lower()
    ]
    
    if exercise_data.empty:
        return 0.0
    
    # Finde das letzte Trainings-Eintrag
    last_weight = exercise_data['weight'].iloc[-1]
    
    # Berechne das neue Gewicht mit Progression (2.5% Erhöhung)
    suggested_weight = calculate_progression(last_weight)
    
    # Runde auf 0.5 kg (Standard-Platteneinteilung)
    if suggested_weight is not None:
        suggested_weight = round(suggested_weight * 2) / 2
    
    return suggested_weight