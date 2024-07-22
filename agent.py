from groq import Groq
import streamlit as st
import agentops, os
from multion.client import MultiOn
from mem0 import Memory

@app.get("/completion")
def completion():

    session = agentops.start_session()

    messages = [{"role": "user", "content": "Hello"}]
    response = session.patch(openai.chat.completions.create)(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
    )

    session.record(
        ActionEvent(
            action_type="Agent says hello",
            params=messages,
            returns=str(response.choices[0].message.content),
        ),
    )

    session.end_session(end_state="Success")

    return {"response": response}

if __name__ == '__main__':
    print("Started!")
    
    # AGENT OPS
    agent_ops_key = st.secrets['agent_ops_key']
    session.start_session(agent_ops_key)
    session.end_session(end_state="Success")

    USER_ID = "facebook_admin"

    # Set up OpenAI API key
    OPEN_AI_KEY = st.secrets['open_ai_key']


    st.write("AI AGENT")
    st.caption("Network Security")

    # st.image("image.png")

    st.write("""
    ### Network Cybersecurity Agent that helps you define better secure network rules.*
    """)

    # Initialize Mem0
    # memory = Memory()

    # Define user data
    USER_DATA = """
    About me
    - I'm facebook network admin, i define network policy on acl.
    """

    # Add Mem0
    #
    # command = "Find commands that I should know to configure network policy"
    #
    # # relevant_memories = memory.search(command, user_id=USER_ID, limit=3)
    # # relevant_memories_text = '\n'.join(mem['text'] for mem in relevant_memories)
    # # print(f"Relevant memories:")
    # # print(relevant_memories_text)
    #
    # # Add user data to memory
    # memory.add(USER_DATA, user_id=USER_ID)
    # print("User data added to memory.")


    with st.form('my_form'):
        text = st.text_area('Enter any Network configuration or security rule code:', 'Enter any Network configuration ?')
        submitted = st.form_submit_button('Submit')
        client = Groq(
            api_key= st.secrets['groq_key'],
        )
        # Fetch llm response
        response = fetch_response(client, text)

        print(response)
        st.markdown(response)

        multion = MultiOn(api_key = st.secrets['multi_on_key'])
        browse = multion.browse(
            cmd="try to access the link and provide status as yes or no if you are able to access the link ",
            url="https://google.com"
        )

        st.write("""
          #### Browse response from multi on:"
          """)
        print("Browse response from multi on:", browse)
        st.markdown(browse)

        print("Ended !!")
