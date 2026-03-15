import streamlit as st
import requests
from PIL import Image
import json
import os

# Page config
st.set_page_config(
    page_title="Plant Care Card Generator",
    layout="wide"
)

API_URL = os.getenv("API_URL", "http://api:8000")

# Title and description
st.title("Plant Care Card Generator")
st.markdown("Upload a plant image to get classification and detailed care instructions")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info(
        "This app uses a VGG11 deep learning model to classify plants "
        "and an AI agent to generate comprehensive care instructions."
    )

    st.header("How to use")
    st.markdown("""
    1. Upload a plant image
    2. Wait for classification
    3. View the care card
    """)

    # Check API health
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("API Connected")
        else:
            st.error("API Error")
    except:
        st.error("API Offline - Start the API first")
        st.code("python main.py")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Upload Image")
    uploaded_file = st.file_uploader(
        "Choose a plant image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload a clear image of your plant"
    )

    if uploaded_file:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Predict button
        if st.button("Identify Plant & Generate Care Card", type="primary", use_container_width=True):
            with st.spinner("Analyzing plant... This may take a minute..."):
                try:
                    # Send request to API
                    files = {"file": uploaded_file.getvalue()}
                    response = requests.post(
                        f"{API_URL}/predict",
                        files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.result = result
                        st.session_state.show_result = True
                        st.rerun()
                    else:
                        st.error(f"Error: {response.text}")

                except Exception as e:
                    st.error(f"Failed to connect to API: {str(e)}")
                    st.info("Make sure the API is running: python main.py")

with col2:
    st.header("Results")

    if "show_result" in st.session_state and st.session_state.show_result:
        result = st.session_state.result

        # Prediction info
        st.subheader("Classification")
        st.success(f"**Plant:** {result['predicted_plant']}")
        st.info(f"**Confidence:** {result['confidence']}")

        st.divider()

        # Care card
        st.subheader("Plant Care Card")
        care_card = result['care_card']

        # Basic info
        with st.expander("Basic Information", expanded=True):
            st.write(f"**Scientific Name:** {care_card['latin_name']}")
            st.write(f"**Common Names:** {', '.join(care_card['common_names'])}")
            st.write(f"**Family:** {care_card['plant_family']}")
            st.write(f"**Native Region:** {care_card['native_region']}")

        # Growing conditions
        with st.expander("Growing Conditions", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Outdoors:** {'Yes' if care_card['outdoors'] else 'No'}")
                st.write(f"**Indoor:** {'Yes' if care_card['indoor_suitable'] else 'No'}")
            with col_b:
                st.write(f"**Lighting:** {care_card['lighting_conditions']}")
                st.write(f"**Temperature:** {care_card['temperature_range']}")
            st.write(f"**Humidity:** {care_card['humidity_requirements']}")

        # Care instructions
        with st.expander("Care Instructions", expanded=True):
            st.write(f"**Watering:** {care_card['watering_schedule']}")
            st.write(f"**Soil:** {care_card['soil_type']}")
            st.write(f"**Fertilization:** {care_card['fertilization']}")
            st.write(f"**Pruning:** {care_card['pruning_needs']}")

        # Additional info
        with st.expander("Additional Information"):
            st.write(f"**Growth Rate:** {care_card['growth_rate']}")
            st.write(f"**Mature Size:** {care_card['mature_size']}")
            st.write(f"**Toxicity:** {care_card['toxicity']}")
            st.write(f"**Common Pests:** {', '.join(care_card['common_pests'])}")

        # Special care notes
        with st.expander("Special Care Notes"):
            st.write(care_card['special_care_notes'])

        st.divider()

        # Download JSON
        if st.button("Download Care Card (JSON)", use_container_width=True):
            json_str = json.dumps(care_card, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"{result['predicted_plant'].replace(' ', '_')}_care_card.json",
                mime="application/json"
            )

    else:
        st.info("Upload an image to get started")

# Footer
st.divider()
st.caption("Powered by VGG11 + OpenAI GPT-4o-mini + Langchain")