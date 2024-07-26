from groq import Groq
import streamlit as st
import agentops, os
from multion.client import MultiOn
from mem0 import Memory


# AGENT OPS CODE FOR RECORDING RESPONSES FROM THE LLM
@agentops.record_function('llm response')
def fetch_response(client, text):
    chat_completion = client.chat.completions.create(
        messages=[
            # SYSTEM MESSAGE 
            # Define the behavior of the Agent for the conversation.
            {
                "role": "system",
                "content": "You are a UX Design consultant specializing in interface improvements for digital products. When a user submits a mockup or wireframe of a user interface, You need to analyze it for usability issues, highlight problematic areas, and provide suggestions on how to optimize and improve the design to enhance user experience. Follow these instructions for your output: 1. Identify and explain usability issues in the submitted design. 2. Offer 3-5 specific suggestions for improving the design. 3. Conduct a brief competitive analysis, comparing the design to similar features in top products, presented in a table format. 4. Provide examples of how specific elements could be improved, with before and after comparisons. 5. Create a user flow diagram to illustrate the ideal interaction path. 6. If the design uses generic placeholders (e.g. Lorem ipsum), recommend ways to make the content more realistic and user-centric. 7. If multiple, disconnected elements are present, suggest ways to organize them for better visual hierarchy. 8. Generate a list of 10-15 usability heuristics that could be used to evaluate the design. 9. Apply these heuristics to the design and create a table showing how well it meets each criterion. 10.Suggest how the design can be further optimized to address any remaining usability concerns identified in the heuristic evaluation."
            },
            # USER MESSAGE FOR THE AGENT TO RESPOND TO
            {
                "role": "user",
                "content": f'user input is {text}',
            }
        ],

        # LLM 
        model="llama3-8b-8192",

        # TEMPERATURE
        # As it approaches zero, the model will become deterministic & repetitive.
        temperature=0.3,

        # MAXIMUM TOKENS
        # 32,768 tokens shared between prompt and completion.
        max_tokens=1000,

        # DIVERSITY
        # Nucleus sampling: 0.5 means half of all weighted options are considered.
        top_p=1,

        # STOP SEQUENCE
        # User-specified text string that signals an AI to stop generating content, 
        # ensuring its responses remain focused and concise. Include punctuation marks
        # and markers like "[end]".
        stop=None,

        # STREAM
        # If set to True, partial message deltas will be sent.
        stream=False,
    )

    response = chat_completion.choices[0].message.content
    return response
    
    agentops.end_session('Success')
    
if __name__ == '__main__':
    print("Started!")
    
    # AGENT OPS API KEY
    agent_ops_key = st.secrets['agent_ops_key'] 

    USER_ID = "Researcher" #facebook_admin

    # OPENAI API KEY
    OPEN_AI_KEY = st.secrets['open_ai_key']

    # CONTENT
    st.write("AI AGENT")
    st.caption("Utilizing AgentOps for recording.")

    # st.image("image.png")

    st.write("""
    ### AI Agent that helps you complete a defined task list.
    """)

    # Initialize Mem0
    # memory = Memory()

    # Define user data
    USER_DATA = """
    About me
    - I'm researcher, I discover order in what appears to be chaos.
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



    # USE GROQ TO COLLECT FORM DATA AND FETCH A RESPONSE
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

        # MULTION API KEY
        multion = MultiOn(api_key = st.secrets['multi_on_key'])
        browse = multion.browse(
            cmd="try to access the link and provide status as yes or no if you are able to access the link ",
            url="https://google.com"
        )

        st.write("""
          #### Browse response from MultiOn:"
          """)
        print("Browse response from MultiOn:", browse)
        st.markdown(browse)

        print("Ended !!")
