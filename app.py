"""
Ladakh Travel Agent — Streamlit Chat Interface
"""

import streamlit as st
from agent.core import create_agent

st.set_page_config(
    page_title="Ladakh Travel Agent 🏔️",
    page_icon="🏔️",
    layout="centered",
)

st.title("🏔️ Ladakh Travel Agent")
st.caption("Your AI guide to planning the perfect Ladakh trip")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Julley! 🙏 I'm your Ladakh Travel Assistant. I can help you with:\n\n"
                "- 📋 **Permits** — ILP requirements and how to apply\n"
                "- 🌤️ **Weather** — Current conditions and forecasts\n"
                "- 🛣️ **Road Status** — Pass conditions and route info\n"
                "- 🏔️ **Altitude Safety** — AMS prevention and acclimatization\n"
                "- 🏠 **Homestays** — Local accommodation options\n"
                "- 🙏 **Cultural Tips** — Etiquette and local customs\n\n"
                "What would you like to know?"
            ),
        }
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask about permits, weather, routes, homestays..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                agent = create_agent()
                result = agent.invoke({"input": prompt})
                response = result["output"]
            except Exception as e:
                response = (
                    f"Sorry, I encountered an error: {str(e)}\n\n"
                    "Please make sure your GROQ_API_KEY is set in the .env file."
                )
        
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
