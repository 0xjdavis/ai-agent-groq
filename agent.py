import streamlit as st
import agentops
from groq import Groq
from multion.client import MultiOn

# AGENT OPS CODE FOR RECORDING RESPONSES FROM THE LLM
@agentops.record_function('llm response')
def fetch_response(client, text):
    chat_completion = client.chat.completions.create(
        messages=[
            # SYSTEM MESSAGE
            {
                "role": "system",
                "content": """You are a UX Researcher tasked with creating user journey maps based on individual user interviews. As you conduct each interview, follow these guidelines to gather and analyze the information:

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

Use this information to identify patterns, common pain points, and opportunities for improvement across multiple user journeys."""
            },
            # USER MESSAGE FOR THE AGENT TO RESPOND TO
            {
                "role": "user",
                "content": f'user input is {text}',
            }
        ],
        model="llama3-8b-8192",
        temperature=0.3,
        max_tokens=1000,
        top_p=1,
        stop=None,
        stream=False,
    )
    
    response = chat_completion.choices[0].message.content
    return response

agentops.end_session('Success')

def main():
    print("Started!")

    # Setting page layout
    st.set_page_config(
        page_title="AI Agent",
        page_icon="✨",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Sidebar for API Key and User Info
    st.sidebar.header("About App")
    st.sidebar.markdown('This is an AI Agent that uses Groq with the llama3-8b-8192 model which completes a workflow using AgentOps and MultiOn created by <a href="https://ai.jdavis.xyz" target="_blank">0xjdavis</a>.', unsafe_allow_html=True)

    # Calendly
    st.sidebar.markdown("""
        <hr />
        <center>
        <div style="border-radius:8px;padding:8px;background:#fff";width:100%;">
        <img src="https://avatars.githubusercontent.com/u/98430977" alt="Oxjdavis" height="100" width="100" border="0" style="border-radius:50%"/>
        <br />
        <span style="height:12px;width:12px;background-color:#77e0b5;border-radius:50%;display:inline-block;"></span> <b>I'm available for new projects!</b><br />
        <a href="https://calendly.com/0xjdavis" target="_blank"><button style="background:#126ff3;color:#fff;border: 1px #126ff3 solid;border-radius:8px;padding:8px 16px;margin:10px 0">Schedule a call</button></a><br />
        </div>
        </center>
        <br />
    """, unsafe_allow_html=True)

    # Copyright
    st.sidebar.caption("©️ Copyright 2024 J. Davis")

    # CONTENT
    st.title("AI Agent")
    st.write("This is an AI Agent using Groq that helps you complete a defined workflow.")

    # Initialize session state for text area
    if 'text_area' not in st.session_state:
        st.session_state.text_area = ""

    # Create a button outside the form
    if st.button("Populate with Example Text"):
        example_text = """This is an example text.
It demonstrates how to populate a text area
with multiple lines of text when a button is clicked.

You can add as much text as you want here!"""
        st.session_state.text_area = example_text

    # USE GROQ TO COLLECT FORM DATA AND FETCH A RESPONSE
    with st.form('my_form'):
        text = st.text_area("Enter your user interview transcripts", value=st.session_state.text_area, height=200)
        submitted = st.form_submit_button('Submit')

        if submitted:
            client = Groq(api_key=st.secrets['groq_key'])
            # Fetch llm response
            response = fetch_response(client, text)

            print(response)
            st.markdown(response)

            # MULTION API KEY
            multion = MultiOn(api_key=st.secrets['multi_on_key'])
            # Browse internet
            browse = multion.browse(
                cmd="Use the url to access the Figma FigJam board file. You have editing privelages to the file. Go to Figma, and create UX Journey Map in FigJam based on the user interviews",
                url="https://www.figma.com/board/TTnCP5XuMHVn4wMjHfQKL1/Automation-Test?node-id=0-1&t=8OVEKUlwDzlAiG5x-0"
            )

            st.write("""
            #### MultiOn:
            """)
            print("Response:", browse)
            st.markdown(browse)

    print("Ended !!")

if __name__ == '__main__':
    main()
