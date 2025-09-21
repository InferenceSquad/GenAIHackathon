import warnings
import streamlit as st
import time

warnings.filterwarnings('ignore')

with open("ui/styles.md", "r") as styles_file:
    styles_content = styles_file.read()

st.write(styles_content, unsafe_allow_html=True)

def initialize_session_state():
    st.session_state.setdefault("departure_place", "")
    st.session_state.setdefault("departure_date", None)
    st.session_state.setdefault("type_of_holiday", "Adventure")
    st.session_state.setdefault("trip_budget", "Economy")
    st.session_state.setdefault("no_of_days", 3)
    st.session_state.setdefault("plan_initiated", False)
    st.session_state.setdefault("adult_count", 1)
    st.session_state.setdefault("child_count", 0)
    st.session_state.setdefault("infant_count", 0)
initialize_session_state()

st.sidebar.title("🧳 Travel Itinerary Planner")
# Display the option to choose the LLM Model
departure_place = st.sidebar.text_input("Enter your departure place:", value=st.session_state.departure_place)
st.session_state["departure_place"] = departure_place

departure_date = st.sidebar.date_input("Enter your departure date:", value=st.session_state.departure_date)
st.session_state["departure_date"] = departure_date

type_of_holiday = st.sidebar.selectbox(
    "Select the type of holiday:", options=["Adventure", "Relaxation", "Cultural", "Family", "Romantic"], index=["Adventure", "Relaxation", "Cultural", "Family", "Romantic"].index(st.session_state.type_of_holiday))
st.session_state["type_of_holiday"] = type_of_holiday

trip_budget = st.sidebar.radio(
    "Select your budget range:", options=["Economy", "Mid-range", "Luxury"], index=["Economy", "Mid-range", "Luxury"].index(st.session_state.trip_budget))
st.session_state["trip_budget"] = trip_budget

no_of_days = st.sidebar.number_input("Select the number of days for your trip:", min_value=1, value=st.session_state.no_of_days)
st.session_state["no_of_days"] = no_of_days

adult_count, child_count, infant_count = st.sidebar.columns(3)
with adult_count:
    st.number_input("Adult", min_value=1, value=st.session_state.adult_count, key="adult_count")
with child_count:
    st.number_input("Child", min_value=0, value=st.session_state.child_count, key="child_count")
with infant_count:
    st.number_input("Infant", min_value=0, value=st.session_state.infant_count, key="infant_count")

# Add Plan Itinerary button as the last sidebar element
plan_btn = st.sidebar.button("Plan Itinerary")
if plan_btn:
    st.session_state["plan_initiated"] = True
    # Read trip itinerary file and set as initial bot message
    with open("mockup_data/trip_itinerary.md", "r", encoding="utf-8") as f:
        itinerary_content = f.read()
    st.session_state["messages"] = [{"role": "assistant", "content": itinerary_content}]

def render_chat_interface():
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and st.session_state.get("plan_initiated") and "trip_itinerary_streamed" not in st.session_state:
                # Stream the itinerary content character by character
                full_content = message["content"]
                streamed_content = ""
                msg_placeholder = st.empty()
                for char in full_content:
                    streamed_content += char
                    msg_placeholder.markdown(streamed_content)
                    time.sleep(0.005)  # Adjust speed as needed
                st.session_state["trip_itinerary_streamed"] = True
            else:
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input(""):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

if st.session_state["plan_initiated"]:
    render_chat_interface()