from groq import Groq
import streamlit as st
import agentops, os
from multion.client import MultiOn
from mem0 import Memory


@agentops.record_function('llm response')
def fetch_response(client, text):
    agentops.start_session()
    chat_completion = client.chat.completions.create(
        
        
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "you are a network security agent. when a user enters the any network commands to configure network rules you need to check if it is invalid and highlight text invalid it with red color, also provide suggestion how to optimize it and update it to make it more concrete and better. follow the instruction for output: 1. Provide info on what is wrong in network rules command. 2. suggest in few command suggestion how to improve it. 3. do a peer review how those network rules are used best way in top companies creating a table comparision.4. Add some examples how rule can be improved  5. Generate some flow chart to explain flow to user. 6. if the user provides any as source or destination then suggest recommedation to optimize it with examples. 7. if user provide multiple ips in source and destination then try to add them in common subnet 8. Create a list of 20 penetration testing url and sub domain urls that could be used to test the network rule. 9. apply all url and generate the table report to indicate how many of them are allowed after the network rule is updated. 10. suggest how rules can be optimized so that no pentration testing url can be allowed."
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": f'user input is {text}',
            }
        ],

        # The language model which will generate the completion.
        model="llama3-8b-8192",

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.3,

        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_tokens=10000,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,

        
        agentops.end_session(end_state='Success')
    )

    response = chat_completion.choices[0].message.content
    return response
    
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
