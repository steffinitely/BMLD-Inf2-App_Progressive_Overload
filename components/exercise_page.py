import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from functions.progression import get_suggested_weight


class ExercisePage:
    def __init__(self, exercise_name):
        self.exercise_name = exercise_name
        self.data_df = st.session_state.get("data_df", pd.DataFrame())

    # =========================
    # 📊 DATA
    # =========================

    def get_exercise_data(self):
        if self.data_df.empty or "exercise" not in self.data_df.columns:
            return pd.DataFrame()

        return self.data_df[
            self.data_df["exercise"].str.lower() == self.exercise_name.lower()
        ]

    # =========================
    # 🎯 TODAY RECOMMENDATION (NEW)
    # =========================

    def render_today_recommendation(self):
        suggestion = get_suggested_weight(self.exercise_name, self.data_df)

        weight = float(suggestion.get("weight", 0.0))
        action = suggestion.get("action", "")
        reason = suggestion.get("reason", "")
        est_1rm = suggestion.get("estimated_1rm", 0)

        st.subheader("🎯 Heute dein Training")

        st.metric(
            label="Empfohlenes Startgewicht",
            value=f"{weight} kg"
        )

        # Coach Feedback
        if action == "increase_weight":
            st.success("💪 Heute kannst du steigern!")
        elif action == "increase_reps":
            st.info("🔁 Fokus: mehr Wiederholungen")
        elif action == "repeat":
            st.warning("➡️ Gewicht beibehalten")
        elif action == "deload":
            st.error("⚠️ Deload empfohlen")

        # Zusatzinfo (1RM)
        if est_1rm:
            st.caption(f"📈 Geschätztes 1RM: {round(est_1rm, 1)} kg")

        st.divider()

    # =========================
    # 📊 CHART
    # =========================

    def render_chart(self, df):
        if df.empty:
            return

        df = df.sort_values("timestamp", ascending=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["timestamp"],
            y=df["weight"],
            mode="lines+markers",
            name="Gewicht"
        ))

        fig.update_layout(
            title="Gewichtsverlauf",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # 📋 TABLE
    # =========================

    def render_table(self, df):
        if df.empty:
            return

        df_display = df[[
            "timestamp", "weight", "reps", "sets", "difficulty"
        ]].copy()

        df_display = df_display.sort_values(
            "timestamp", ascending=False
        ).head(10)

        df_display.columns = [
            "Datum", "Gewicht (kg)", "Reps", "Sets", "Schwierigkeit"
        ]

        st.dataframe(df_display, use_container_width=True, hide_index=True)

    # =========================
    # ➕ INPUT FORM
    # =========================

    def render_input(self):
        suggestion = get_suggested_weight(self.exercise_name, self.data_df)
        suggested_weight = float(suggestion.get("weight", 0.0))

        st.subheader("➕ Neues Training erfassen")

        col1, col2, col3 = st.columns(3)

        with col1:
            weight = st.number_input(
                "Gewicht",
                min_value=0.0,
                step=0.5,
                format="%.1f",
                value=suggested_weight
            )

        with col2:
            reps = st.number_input(
                "Reps",
                min_value=1,
                step=1,
                value=8
            )

        with col3:
            sets = st.number_input(
                "Sets",
                min_value=1,
                step=1,
                value=3
            )

        difficulty = st.select_slider(
            "Schwierigkeit",
            options=[
                "Sehr einfach",
                "Einfach",
                "Gut",
                "Schwierig",
                "Sehr schwierig"
            ],
            value="Gut"
        )

        return weight, reps, sets, difficulty

    # =========================
    # 💾 SAVE
    # =========================

    def save(self, weight, reps, sets, difficulty):
        from utils.data_manager import DataManager

        record = {
            "exercise": self.exercise_name,
            "weight": float(weight),
            "reps": int(reps),
            "sets": int(sets),
            "difficulty": difficulty
        }

        self.data_df = DataManager.append_record(
            self.data_df,
            record
        )

        st.session_state["data_df"] = self.data_df

        DataManager().save_user_data(
            self.data_df,
            "data.csv"
        )

    # =========================
    # 🚀 MAIN RENDER
    # =========================

    def render(self):
        st.title(f"🏋️ {self.exercise_name}")

        # 🔥 NEW: Coach Recommendation zuerst
        self.render_today_recommendation()

        df = self.get_exercise_data()

        if not df.empty:
            st.subheader("📊 Fortschritt")
            self.render_table(df)
            self.render_chart(df)
        else:
            st.info("Noch keine Daten vorhanden")

        st.divider()

        weight, reps, sets, difficulty = self.render_input()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Speichern", use_container_width=True):
                self.save(weight, reps, sets, difficulty)
                st.success("Gespeichert!")
                st.rerun()

        with col2:
            if st.button("❌ Abbrechen", use_container_width=True):
                st.rerun()