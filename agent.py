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
                "content": """
You are a UX Researcher tasked with creating user journey maps based on individual user interviews. 
As you conduct each interview, follow these guidelines to gather and analyze the information:

1. Document the user's key touchpoints and interactions with the product or service throughout their experience.
2. Identify and note any pain points, frustrations, or areas of confusion the user encounters during their journey.
3. Highlight positive experiences and moments of delight expressed by the user.
4. Create a timeline of the user's journey, capturing the sequence of events and actions taken.
5. Note the user's emotions and thoughts at each stage of their journey.
6. Identify any gaps in the user's experience or missed opportunities for engagement.
7. Document any workarounds or alternative methods the user employs to accomplish their goals.
8. Capture quotes or specific language used by the user to describe their experience.
9. Note any external factors or influences that impact the user's journey.
10. Identify key decision points in the user's journey and the factors influencing those decisions.
11. Document the user's goals and motivations at different stages of their journey.
12. Capture any suggestions or improvements proposed by the user.
13. Note any differences between the intended user journey and the actual experience described by the user.
14. Identify touchpoints where the user interacts with different channels or devices.
15. Document any points where the user seeks help or additional information.
16. Note instances where the user's expectations are either met or not met.
17. Capture any moments of uncertainty or hesitation in the user's journey.
18. Identify opportunities for personalization or customization in the user's experience.
19. Document any social or collaborative aspects of the user's journey.
20. Note how the user's journey aligns with or differs from your initial assumptions or hypotheses.

After each interview, create a visual diagram or flow chart showing the user's journey and make sure it highlights the key touchpoints and interactions and maps each user's journey through the flow, providing a comprehensive view of the user's experience. 
Use this information to identify patterns, common pain points, and opportunities for improvement across multiple user journeys.
                """
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
        text = st.text_area('Enter your user interview transcripts', 'Enter your user interview transcripts.')
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
        # Browse internet
        browse = multion.browse(
            cmd="Go to Figma, and create UX Journey Map in FigJam based on the user interviews",
            url="https://www.figma.com/board/Dp7xuoZn2u9ij1iBgR2yRJ/Untitled?t=qyeEJhCW13xyu3Ls-6"
        )

        st.write("""
          #### Browse response from MultiOn:"
          """)
        print("Browse response from MultiOn:", browse)
        st.markdown(browse)

        print("Ended !!")
