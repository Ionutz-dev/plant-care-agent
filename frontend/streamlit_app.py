import streamlit as st
import requests
from PIL import Image
import json
import os

# 1. Page config - Added an icon and ensured sidebar starts open
st.set_page_config(
    page_title="Plant Care Card",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Optional: Add a bit of custom CSS to reduce excessive top padding
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://api:8000")

# Title and description
st.title("🌿 Plant Care Card Generator")
st.markdown("Upload a photo of any plant to instantly receive classification details and a personalized care guide.")
st.divider()

# Sidebar
with st.sidebar:
    st.header("About")
    st.write(
        "Powered by a **VGG11** deep learning model for classification "
        "and an **AI agent** for generating comprehensive care instructions."
    )

    st.header("How to use")
    st.markdown("""
    1. **Upload** a clear image of a plant.
    2. **Click** the generate button.
    3. **Explore** the care tabs.
    """)

    st.divider()

    # Cleaner API status indicator
    st.subheader("System Status")
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("🟢 API Online")
        else:
            st.warning("🟡 API Error")
    except:
        st.error("🔴 API Offline")
        st.caption("Start the API first:")
        st.code("python main.py")

# Main content - Added 'gap' for better spacing
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader(
        "Choose a plant image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"  # Hides redundant label for cleaner UI
    )

    if uploaded_file:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)

        # Predict button - Updated styling
        if st.button("✨ Identify Plant & Generate Guide", type="primary", use_container_width=True):
            with st.spinner("Analyzing plant... This may take a moment..."):
                try:
                    # Send request to API
                    response = requests.post(
                        f"{API_URL}/predict",
                        files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    )

                    if response.status_code == 200:
                        st.session_state.result = response.json()
                        st.session_state.show_result = True
                        st.rerun()
                    else:
                        st.error(f"Error: {response.text}")

                except Exception as e:
                    st.error(f"Failed to connect to API: {str(e)}")
                    st.info("Make sure the API is running: `python main.py`")

with col2:
    st.subheader("Result")

    if "show_result" in st.session_state and st.session_state.show_result:
        result = st.session_state.result
        care_card = result.get('care_card', {})

        # Use columns for plant name and a clean metric component for confidence
        r_col1, r_col2 = st.columns([3, 1])
        with r_col1:
            st.header(result.get('predicted_plant', 'Unknown Plant').title())
        with r_col2:
            st.metric(label="Confidence Score", value=result.get('confidence', 'N/A'))

        # Use Tabs instead of multiple Expanders to save vertical space
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "🌱 Care Needs", "ℹ️ Details", "💡 Notes"])

        with tab1:
            st.markdown(f"**Scientific Name:** _{care_card.get('latin_name', 'N/A')}_")
            st.markdown(f"**Common Names:** {', '.join(care_card.get('common_names', ['N/A']))}")
            st.markdown(f"**Family:** {care_card.get('plant_family', 'N/A')}")
            st.markdown(f"**Native Region:** {care_card.get('native_region', 'N/A')}")

            # Inline badges for indoor/outdoor compatibility
            outdoors = "✅ Yes" if care_card.get('outdoors') else "❌ No"
            indoor = "✅ Yes" if care_card.get('indoor_suitable') else "❌ No"
            st.divider()
            st.markdown(f"**Suitable Outdoors:** {outdoors} &nbsp;&nbsp;|&nbsp;&nbsp; **Suitable Indoors:** {indoor}")

        with tab2:
            st.markdown(f"**☀️ Lighting:** {care_card.get('lighting_conditions', 'N/A')}")
            st.markdown(f"**🌡️ Temperature:** {care_card.get('temperature_range', 'N/A')}")
            st.markdown(f"**💧 Humidity:** {care_card.get('humidity_requirements', 'N/A')}")
            st.markdown(f"**🚿 Watering:** {care_card.get('watering_schedule', 'N/A')}")
            st.markdown(f"**🪨 Soil:** {care_card.get('soil_type', 'N/A')}")
            st.markdown(f"**🧪 Fertilization:** {care_card.get('fertilization', 'N/A')}")
            st.markdown(f"**✂️ Pruning:** {care_card.get('pruning_needs', 'N/A')}")

        with tab3:
            st.markdown(f"**📈 Growth Rate:** {care_card.get('growth_rate', 'N/A')}")
            st.markdown(f"**📏 Mature Size:** {care_card.get('mature_size', 'N/A')}")
            st.markdown(f"**☠️ Toxicity:** {care_card.get('toxicity', 'N/A')}")
            st.markdown(f"**🐛 Common Pests:** {', '.join(care_card.get('common_pests', ['N/A']))}")

        with tab4:
            st.info(care_card.get('special_care_notes', 'No special notes available.'))

        st.divider()

        # Download JSON button (full width)
        json_str = json.dumps(care_card, indent=2)
        st.download_button(
            label="Download Care Card (JSON)",
            data=json_str,
            file_name=f"{result.get('predicted_plant', 'plant').replace(' ', '_')}_care_card.json",
            mime="application/json",
            use_container_width=True
        )

    else:
        # Empty state prompt
        st.info("Upload an image and click **Identify Plant** to see the care guide here.")

# Footer
st.divider()
st.caption("Powered by VGG11 + OpenAI GPT-4o-mini + Langchain")