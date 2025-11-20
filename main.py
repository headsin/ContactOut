import streamlit as st
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")

def get_profile(linkedin_url):
    headers = {
        "Accept": "application/json",
        "token": API_KEY
    }
    params = {"profile": linkedin_url,"include": "phone"}

    resp = requests.get(ENDPOINT, headers=headers, params=params)

    if resp.status_code != 200:
        st.error(f"Error {resp.status_code} → {resp.text}")
        return None

    return resp.json()

st.header("ContactOut Enrichment")

url = st.text_input("Enter LinkedIn URL:")

if st.button("Get Profile"):
    data = get_profile(url)

    if not data:
        st.stop()

    profile = data.get("profile")
    
    with st.expander(profile.get("full_name", "Profile"), expanded=False):
        st.json(profile)

    # MAIN CONTAINER
    with st.expander(profile.get("full_name", "Profile"), expanded=True):

        col1, col2 = st.columns([1, 2])

       
        with col1:
            # Profile image
            img = profile.get("profile_picture_url") or "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDVO09x_DXK3p4Mt1j08Ab0R875TdhsDcG2A&s"
            st.image(img, width=150)

            # Name
            st.subheader(profile.get("full_name", "Unknown"))

            # Headline
            if profile.get("headline"):
                st.write(profile["headline"])

            # Phone numbers
            phones = profile.get("phone", [])
            st.markdown("### Phone")
            if phones:
                for p in phones:
                    st.write(f"{p}")
            else:
                st.write("Not available")

        
        with col2:
            # ABOUT / SUMMARY
            st.markdown("### About")
            st.write(profile.get("summary", "Not provided"))

            # EXPERIENCE
            st.markdown("### Experience")
            experience_list = profile.get("experience", [])

            if experience_list:
                for exp in experience_list:
                    st.markdown(f"**{exp.get('title', 'Unknown Role')}** — {exp.get('company_name', '')}")
                    date_range = f"{exp.get('start_date_year', '')} - {exp.get('end_date_year', '') or 'Present'}"
                    st.write(date_range)
                    st.markdown("---")
            else:
                st.write("No experience found")
