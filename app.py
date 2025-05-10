import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Conversational Assistant", layout="centered")

st.markdown("<p style='font-size: 3em; font-weight: bold;'>Welcome to xxx</p>", unsafe_allow_html=True)

st.markdown("""
<p style="color: white; font-size: 18px;">
This app allows you to interact with two main features:
<ul>
    <li>📄 <strong>Document Question Answering</strong>: Upload documents, process them, and ask questions about their content.</li>
    <li>📅 <strong>Appointment Booking</strong>: Book an appointment by providing details like your name, email, phone, and preferred date.</li>
</ul>
</p>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="display: flex; justify-content: space-between;">
        <div style="background-color: #3498db; padding: 20px; border-radius: 8px; width: 48%; color: white;">
            <p style='font-size: 1.5em; font-weight: bold;'>Document QA:</p>
            <ul>
                <li>Upload documents (PDF, TXT, DOCX).</li>
                <li>Process them for querying specific information.</li>
            </ul>
        </div>
        <div style="background-color: #e74c3c; padding: 20px; border-radius: 8px; width: 48%; color: white;">
            <p style='font-size: 1.5em; font-weight: bold;'>Appointment Booking:</p>
            <ul>
                <li>Provide your name, email, phone, and preferred date.</li>
                <li>Complete the conversational flow for booking.</li>
            </ul>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p style='font-size: 2em; font-weight: bold;'>Instructions:</p>
    <ol style="color: white; font-size: 18px; line-height: 1.6;">
        <li>Use the sidebar to select between the two pages: <strong>Document QA</strong> or <strong>Appointment Booking</strong>.</li>
        <li>For <strong>Document QA</strong>, upload your documents (PDF, TXT, DOCX) and then you can query them for specific information.</li>
        <li>For <strong>Appointment Booking</strong>, follow the conversational flow to provide your details, including your name, contact information, preferred appointment date, and purpose.</li>
    </ol>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
<div style="background-color: #2C3E50; padding: 10px; border-radius: 5px; color: white; text-align: center;">
    Choose a feature from the sidebar to get started and interact with the app!
</div>
""", unsafe_allow_html=True)
