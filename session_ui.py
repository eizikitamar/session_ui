import streamlit as st
import requests

# Define the API endpoint
API_URL = "https://whatsapp-he.secretflights.co.il/api/v1/chat/history/session/"
# session_id = '7a367293-7945-4090-a692-eeec72aa279b'

def get_conversation(session_id):
    try:
        headers = {
            'Accept': 'application/json',
        }
        response = requests.get(API_URL + session_id, headers=headers)
        if response.status_code == 200:
            conversation = response.json()
            return conversation
        else:

            st.error(f"Failed to fetch conversation. Please try again later. {response.url}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    session_id = st.query_params['session_id']
    # Fetch conversation data from the API
    conversation = get_conversation(session_id)

    if conversation:
        api_payload = conversation

        # Sidebar with name and number
        st.sidebar.subheader("Name and Number")
        st.sidebar.write(f"ID: {api_payload['id']}")
        st.sidebar.write(f"Client ID: {api_payload['client_id']}")
        st.sidebar.write(f"User ID: {api_payload['user_id']}")

        # Display conversation
        st.subheader("Conversation")
        for event in api_payload['events']:
            sender = "Client" if event['incoming'] else "Agent"
            color = "blue" if event['incoming'] else "green"
            st.markdown(
                f'<div style="text-align: right; direction: rtl;"><span style="color:{color}">{sender}:</span> {event["text"]}</div>',
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()
