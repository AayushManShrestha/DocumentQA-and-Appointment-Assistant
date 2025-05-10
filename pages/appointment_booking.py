import streamlit as st
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from utils.date_utils import parse_natural_date
from config.llm import llm
from utils.booking_utils import save_booking, step_handlers, next_prompt_for_step
from utils.validator import validate_field


# Initialize session state
def initialize_state():
    if "booking_messages" not in st.session_state:
        st.session_state.booking_messages = []
    if "booking_state" not in st.session_state:
        st.session_state.booking_state = {
            "step": 1,
            "data": {}
        }


# Conversational booking flow
def appointment_booking(user_message):
    state = st.session_state.booking_state
    data = state["data"]
    current_step = state["step"]

    # Handle the current step using step_handlers
    handler = step_handlers.get(current_step)
    if handler:
        reply = handler(user_message, data)
        if reply:
            return reply

    # If all steps are completed, save the booking
    if current_step == 5:
        save_booking(data)
        state["step"] += 1
        reply = (
            f"🎉 Thank you, {data['name']}! Your appointment has been successfully booked.\n\n"
            f"🗓 Appointment details:\n"
            f"Date: {data['date']}\n"
            f"📧 We'll reach out to you at: {data['email']}\n"
            f"📱 Contact number: {data['phone']}\n"
            "We look forward to seeing you!"
        )
        return reply

    if current_step == 6:
        # Reset the state for another potential booking
        state["step"] = 1
        state["data"] = {}
        reply = (
            "Would you like to book another appointment? 😄\n"
            "If so, just provide your details again and we’ll get started! 💬\n\n"
            "Let’s kick things off with your name!"
        )
        return reply

    # Move to the next step
    state["step"] += 1
    return next_prompt_for_step(state["step"])

@tool
def collect_contact_info(query: str) -> dict:
    """Initiate contact information collection process."""
    return {"status": "contact_collection_started"}

@tool
def book_appointment(natural_date: str) -> str:
    """Convert natural language date to YYYY-MM-DD format."""
    parsed_date = parse_natural_date(natural_date)
    return parsed_date if parsed_date else "Invalid date format"

def main():
    st.title("🤖 Smart Booking Assistant")

    # Initialize session state
    initialize_state()

    tools = [collect_contact_info, book_appointment]

    prompt = ChatPromptTemplate.from_messages([  
        ("system", "You are an assistant that helps with booking appointments."),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad")
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    # Display chat history for appointment booking
    for msg in st.session_state.booking_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Start the booking flow if no messages are present
    if len(st.session_state.booking_messages) == 0:
        st.session_state.booking_messages.append({"role": "assistant", "content": "Hello! I'm here to help you book an appointment."})
        st.session_state.booking_messages.append({"role": "assistant", "content": "Let's get started. May I have your full name?"})
        st.rerun()

    # User input for the appointment booking process
    user_input = st.chat_input("Book an appointment.")
    if user_input:
        reply = appointment_booking(user_input)
        st.session_state.booking_messages.append({"role": "user", "content": user_input})
        if reply:
            st.session_state.booking_messages.append({"role": "assistant", "content": reply})
        st.rerun()


if __name__ == "__main__":
    main()
