import streamlit as st
from datetime import datetime, date, timedelta
from supabase_client import supabase_select, supabase_insert, supabase_update
import random

st.set_page_config(page_title="maxBOT", page_icon="🏀", layout="wide")

USER_ID = "maxbot_user"

st.sidebar.title("maxBOT")
st.sidebar.write("Personal Tracker")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", ["Dashboard", "Daily Check-in", "Motivational Quotes", "Basketball Stats", "Reflections", "Other Features"])

st.sidebar.markdown("---")
st.sidebar.info(f"{datetime.now().strftime('%B %d, %Y')}")

if page == "Dashboard":
    st.title("Welcome to maxBOT")
    st.write("Your personal basketball growth and discipline tracker.")
    st.success("App is ready! Start tracking your journey.")
    
    checkins = supabase_select('daily_checkins', {'user_id': f'eq.{USER_ID}'})
    total_checkins = len(checkins)
    
    dates = sorted([c['date'] for c in checkins], reverse=True)
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
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Check-ins", total_checkins)
    with col2:
        st.metric("Current Streak", f"{streak} days")

elif page == "Daily Check-in":
    st.title("Daily Check-in")
    today = str(date.today())
    
    checkins = supabase_select('daily_checkins', {'user_id': f'eq.{USER_ID}', 'date': f'eq.{today}'})
    existing_checkin = checkins[0] if checkins else None
    
    if existing_checkin:
        st.success("Already checked in today!")
        st.write("---")
        st.subheader("Today's Check-in:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Practice", "Yes" if existing_checkin['attended_practice'] else "No")
            st.metric("Avoided Smoking", "Yes" if existing_checkin['avoided_smoking'] else "No")
        with col2:
            st.metric("Avoided Masturbation", "Yes" if existing_checkin['avoided_masturbation'] else "No")
            st.metric("Mood", f"{existing_checkin['mood_rating']}/10")
        st.metric("Energy Level", f"{existing_checkin['energy_level']}/10")
    else:
        st.subheader("Log Your Day")
        
        attended_practice = st.checkbox("I practiced basketball today")
        avoided_masturbation = st.checkbox("I stayed clean")
        avoided_smoking = st.checkbox("I did not smoke today")
        mood_rating = st.slider("Mood", 1, 10, 5)
        energy_level = st.slider("Energy", 1, 10, 5)
        
        if st.button("Save Check-in", type="primary"):
            data = {
                'user_id': USER_ID,
                'date': today,
                'attended_practice': attended_practice,
                'avoided_masturbation': avoided_masturbation,
                'avoided_smoking': avoided_smoking,
                'mood_rating': mood_rating,
                'energy_level': energy_level
            }
            
            if supabase_insert('daily_checkins', data):
                st.success("Saved!")
                st.balloons()
                st.rerun()
            else:
                st.error("Failed to save. Please try again.")

elif page == "Motivational Quotes":
    st.title("Motivational Quotes")
    
    quotes = supabase_select('quotes')
    
    if quotes:
        quote = random.choice(quotes)
        st.markdown(f"### {quote['quote_text']}")
        if quote.get('author'):
            st.markdown(f"**{quote['author']}**")
        if st.button("Another Quote"):
            st.rerun()
    else:
        st.info("No quotes available yet.")

else:
    st.title(page)
    st.write("Coming soon!")
