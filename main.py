import streamlit as st
from datetime import datetime, date, timedelta
from database import get_connection
import random

st.set_page_config(page_title="maxBOT", page_icon="🏀", layout="wide")

USER_ID = "maxbot_user"

st.sidebar.title("maxBOT")
st.sidebar.write("Personal Tracker")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "Dashboard", "Daily Check-in", "Basketball Stats", "Reflections",
    "Motivational Quotes", "To-Do List", "Goals", "Habit Streaks",
    "Progress Photos"
])

st.sidebar.markdown("---")
st.sidebar.info(f"{datetime.now().strftime('%B %d, %Y')}")

if page == "Dashboard":
    st.title("Welcome to maxBOT")
    st.write("Your personal basketball growth and discipline tracker.")
    st.success("App is ready! Start tracking your journey.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM daily_checkins WHERE user_id = ?',
                   (USER_ID, ))
    total_checkins = cursor.fetchone()[0]

    cursor.execute(
        'SELECT date FROM daily_checkins WHERE user_id = ? ORDER BY date DESC',
        (USER_ID, ))
    dates = [row[0] for row in cursor.fetchall()]

    streak = 0
    if dates:
        current_date = date.today()
        for i, check_date in enumerate(dates):
            check_date_obj = date.fromisoformat(check_date)
            expected_date = current_date - timedelta(days=i)
            if check_date_obj == expected_date:
                streak += 1
            else:
                break

    conn.close()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Check-ins", total_checkins)
    with col2:
        st.metric("Current Streak", f"{streak} days")

elif page == "Daily Check-in":
    st.title("Daily Check-in")

    today = str(date.today())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM daily_checkins WHERE user_id = ? AND date = ?',
        (USER_ID, today))
    existing_checkin = cursor.fetchone()

    if existing_checkin:
        st.success("Already checked in today!")
        st.write("---")
        st.subheader("Today's Check-in:")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Practice",
                      "Yes" if existing_checkin['attended_practice'] else "No")
            st.metric("Avoided Smoking",
                      "Yes" if existing_checkin['avoided_smoking'] else "No")
        with col2:
            st.metric(
                "Avoided Masturbation",
                "Yes" if existing_checkin['avoided_masturbation'] else "No")
            st.metric("Mood", f"{existing_checkin['mood_rating']}/10")

        st.metric("Energy Level", f"{existing_checkin['energy_level']}/10")

        if st.button("Edit Check-in"):
            st.session_state.edit_checkin = True
            st.rerun()

    if not existing_checkin or st.session_state.get('edit_checkin', False):
        st.subheader("Log Your Day")

        attended_practice = st.checkbox(
            "I practiced basketball today",
            value=bool(existing_checkin['attended_practice'])
            if existing_checkin else False)
        avoided_masturbation = st.checkbox(
            "I stayed clean",
            value=bool(existing_checkin['avoided_masturbation'])
            if existing_checkin else False)
        avoided_smoking = st.checkbox(
            "I did not smoke today",
            value=bool(existing_checkin['avoided_smoking'])
            if existing_checkin else False)
        mood_rating = st.slider(
            "Mood",
            1,
            10,
            value=existing_checkin['mood_rating'] if existing_checkin else 5)
        energy_level = st.slider(
            "Energy",
            1,
            10,
            value=existing_checkin['energy_level'] if existing_checkin else 5)

        if st.button("Save Check-in", type="primary"):
            if existing_checkin:
                cursor.execute(
                    'UPDATE daily_checkins SET attended_practice=?, avoided_masturbation=?, avoided_smoking=?, mood_rating=?, energy_level=? WHERE id=?',
                    (attended_practice, avoided_masturbation, avoided_smoking,
                     mood_rating, energy_level, existing_checkin['id']))
                st.success("Updated!")
            else:
                cursor.execute(
                    'INSERT INTO daily_checkins (user_id, date, attended_practice, avoided_masturbation, avoided_smoking, mood_rating, energy_level) VALUES (?,?,?,?,?,?,?)',
                    (USER_ID, today, attended_practice, avoided_masturbation,
                     avoided_smoking, mood_rating, energy_level))
                st.success("Saved!")
            conn.commit()
            st.session_state.edit_checkin = False
            st.rerun()

    conn.close()

elif page == "Basketball Stats":
    from page_basketball_stats import show_basketball_stats
    show_basketball_stats(USER_ID)

elif page == "Motivational Quotes":
    st.title("Motivational Quotes")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM quotes')
    quotes = cursor.fetchall()
    conn.close()

    if quotes:
        quote = random.choice(quotes)
        st.markdown(f"### {quote['quote_text']}")
        if quote['author']:
            st.markdown(f"**{quote['author']}**")
        if st.button("Another Quote"):
            st.rerun()

else:
    st.title(page)
    st.write("Coming soon!")
