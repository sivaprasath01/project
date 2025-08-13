import streamlit as st
import pandas as pd
from math import radians, sin, cos, sqrt, asin
import pickle
import time

# Load pre-trained model
model = pickle.load(open('model.pkl', 'rb'))

# Haversine function
def haversine(a):
    lon1, lat1, lon2, lat2 = map(radians, [a[0], a[1], a[2], a[3]])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    calc = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(calc))
    return 6371 * c  # km

# ----------- Page Styling with Background Image -----------
st.set_page_config(page_title="Cab Fare Prediction", page_icon="🚖", layout="centered")

st.markdown("""
    <style>
        /* Remove default white background */
        .stApp {
            background: transparent !important;
        }
        body {
            background-image: url('https://images.unsplash.com/photo-1504215680853-026ed2a45def');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }
        .main-title {
            font-size: 40px;
            font-weight: bold;
            color: white;
            text-align: center;
            text-shadow: 2px 2px 4px #000;
        }
        .sub-title {
            font-size: 20px;
            font-weight: 600;
            margin-top: 10px;
            color: white;
            text-shadow: 1px 1px 2px black;
        }
        .stButton>button {
            background-color: #ff9800;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
            border: none;
        }
        .result-card {
            background-color: rgba(0,0,0,0.6);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: #ffeb3b;
            margin-top: 20px;
            text-shadow: 2px 2px 4px black;
        }
    </style>
""", unsafe_allow_html=True)




# Add ticking sound effect (short mp3 in loop)
st.markdown("""
<audio id="tickSound" src="https://www.soundjay.com/mechanical/camera-shutter-click-01.mp3" preload="auto"></audio>
<script>
function playTick() {
    var sound = document.getElementById('tickSound');
    sound.play();
}
</script>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-title">🚖 Cab Fare Prediction</p>', unsafe_allow_html=True)

# ----------- Input Layout -----------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="sub-title">📍 Pickup & Drop-off</p>', unsafe_allow_html=True)
    pickup_lat = st.number_input('Pickup Latitude', min_value=-90.0, max_value=90.0, value=40.7128)
    pickup_lon = st.number_input('Pickup Longitude', min_value=-180.0, max_value=180.0, value=-74.0060)
    dropoff_lat = st.number_input('Dropoff Latitude', min_value=-90.0, max_value=90.0, value=40.7306)
    dropoff_lon = st.number_input('Dropoff Longitude', min_value=-180.0, max_value=180.0, value=-73.9352)

with col2:
    st.markdown('<p class="sub-title">🕒 Trip Details</p>', unsafe_allow_html=True)
    passenger_count = st.number_input('Passenger Count', min_value=1, max_value=6, value=1)
    year = st.number_input('Year', min_value=2010, max_value=2025, value=2023)
    month = st.number_input('Month', min_value=1, max_value=12, value=4)
    day = st.number_input('Day of the Month', min_value=1, max_value=31, value=4)
    hour = st.number_input('Hour of the Day', min_value=0, max_value=23, value=15)
    minute = st.number_input('Minute of the Hour', min_value=0, max_value=59, value=30)

# Calculate distance
distance = haversine([pickup_lon, pickup_lat, dropoff_lon, dropoff_lat])

# ----------- Prediction Button with Smooth Animated Fare + Ticking Sound -----------
if st.button('Predict Fare 💰'):
    input_data = pd.DataFrame({
        'passenger_count': [passenger_count],
        'year': [year],
        'Month': [month],
        'Date': [day],
        'Day': [0],
        'Hour': [hour],
        'distance': [distance]
    })

    predicted_fare = model.predict(input_data)[0]

    # Smooth Animated Counter (with ticks)
    placeholder = st.empty()
    current_fare = 0.0
    increment = predicted_fare / 100  # 100 small steps

    while current_fare < predicted_fare:
        current_fare += increment
        if current_fare > predicted_fare:
            current_fare = predicted_fare
        placeholder.markdown(
            f'<div class="result-card">Predicted Fare: ${current_fare:.2f}</div>'
            f'<script>playTick();</script>',
            unsafe_allow_html=True
        )
        time.sleep(0.05)  # Speed of animation
