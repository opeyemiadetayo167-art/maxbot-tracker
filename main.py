import streamlit as st
from datetime import datetime
from supabase_client import supabase

# Page configuration
st.set_page_config(page_title="maxBOT", page_icon="🏀", layout="wide")

# Initialize session state for login
if 'user' not in st.session_state:
    st.session_state.user = None


# Authentication Functions
def login(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        st.session_state.user = response.user
        return True, "Login successful!"
    except Exception as e:
        return False, str(e)


def signup(email, password):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return True, "Account created! Please log in."
    except Exception as e:
        return False, str(e)


def logout():
    try:
        supabase.auth.sign_out()
        st.session_state.user = None
        st.success("Logged out successfully!")
    except Exception as e:
        st.error(f"Logout error: {e}")


# Check if user is logged in
if st.session_state.user is None:
    # Login/Signup Page
    st.title("🏀 maxBOT")
    st.subheader("Your Basketball Growth & Discipline Tracker")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login to Your Account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password",
                                 type="password",
                                 key="login_password")

        if st.button("Login"):
            if email and password:
                success, message = login(email, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(f"Login failed: {message}")
            else:
                st.warning("Please enter email and password")

    with tab2:
        st.subheader("Create New Account")
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password (min 6 characters)",
                                     type="password",
                                     key="signup_password")
        confirm_password = st.text_input("Confirm Password",
                                         type="password",
                                         key="confirm_password")

        if st.button("Sign Up"):
            if new_email and new_password and confirm_password:
                if new_password == confirm_password:
                    if len(new_password) >= 6:
                        success, message = signup(new_email, new_password)
                        if success:
                            st.success(message)
                        else:
                            st.error(f"Signup failed: {message}")
                    else:
                        st.warning("Password must be at least 6 characters")
                else:
                    st.warning("Passwords don't match")
            else:
                st.warning("Please fill all fields")

else:
    # User is logged in - Show the app

    # Sidebar Navigation
    st.sidebar.title("🏀 maxBOT")
    st.sidebar.write(f"👤 {st.session_state.user.email}")
    st.sidebar.markdown("---")

    page = st.sidebar.radio("Navigate", [
        "🏠 Dashboard", "✅ Daily Check-in", "📊 Basketball Stats",
        "📝 Reflections", "💪 Motivational Quotes", "📋 To-Do List", "🎯 Goals",
        "🔥 Habit Streaks", "📸 Progress Photos"
    ])

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        logout()
        st.rerun()

    st.sidebar.info(f"📅 {datetime.now().strftime('%B %d, %Y')}")

    # Main Content Area
    if page == "🏠 Dashboard":
        st.title("🏠 Dashboard")
        st.write("Welcome back! Your data is saved to your account.")

    elif page == "✅ Daily Check-in":
        st.title("✅ Daily Check-in")
        st.write("Log your daily activities here")

    elif page == "📊 Basketball Stats":
        st.title("📊 Basketball Stats")
        st.write("Track your basketball performance")

    elif page == "📝 Reflections":
        st.title("📝 Reflections")
        st.write("Journal and reflect on your progress")

    elif page == "💪 Motivational Quotes":
        st.title("💪 Motivational Quotes")
        st.write("Get motivated with hard-hitting quotes")

    elif page == "📋 To-Do List":
        st.title("📋 To-Do List")
        st.write("Manage your tasks")

    elif page == "🎯 Goals":
        st.title("🎯 Goals")
        st.write("Set and track your goals")

    elif page == "🔥 Habit Streaks":
        st.title("🔥 Habit Streaks")
        st.write("Track your habit streaks")

    elif page == "📸 Progress Photos":
        st.title("📸 Progress Photos")
        st.write("Upload and compare progress photos")
