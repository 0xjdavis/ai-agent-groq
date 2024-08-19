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
    if st.button("Paste Example Transcript"):
        example_text = """Interview 1

Interviewer: Hi! Thanks for joining us today. We’re excited to hear your thoughts on the new Google Single Sign-On interface. Let’s dive right in. Can you start by describing your overall experience with the new SSO interface?
User1: Hi! Sure. Overall, it’s been pretty smooth. The new design is clean and straightforward, which I really appreciate. It’s quicker to navigate through the sign-in process compared to the old version.
Interviewer: That’s great to hear! Can you tell me a bit more about what you like about the new design?
User1: I like that the sign-in screen is less cluttered. The key buttons are easy to find, and the interface doesn’t have too many distractions. Also, the visual cues are clearer, so I can easily tell what I need to do next.
Interviewer: Interesting! Were there any specific features or changes that stood out to you?
User1: Yes, the addition of the “Remember Me” option is a big plus. It saves me from having to log in every time I use a new app. I also like the improved error messages—if I make a mistake, it’s much easier to understand what went wrong.
Interviewer: That’s helpful feedback. Did you encounter any challenges or issues while using the new SSO interface?
User1: Not really. One minor issue was that I found the password reset link wasn’t as visible as I expected. It took me a bit longer to find it when I needed it. But other than that, everything worked well.
Interviewer: Thanks for pointing that out. We’ll look into making the password reset option more prominent. How about the speed of the interface? Did you notice any changes?
User1: Yes, the speed has definitely improved. The whole sign-in process feels faster, and pages load more quickly. That’s a big improvement from the old interface, which sometimes felt sluggish.
Interviewer: Excellent, that’s good to hear. How intuitive did you find the new SSO interface? Did you need any help figuring out how to use it?
User1: It was quite intuitive. The interface guides you through the process clearly, and the options are easy to understand. I didn’t need any help, which is a nice change from having to look up instructions.
Interviewer: Fantastic. Is there anything you would suggest to improve the SSO interface further?
User1: Maybe add a small tutorial or walkthrough for first-time users. Even though the interface is intuitive, a brief guide might help new users get acquainted faster.
Interviewer: That’s a great suggestion. We’ll consider adding a walkthrough feature. Thanks so much for your time and feedback today. It’s been really valuable!
User1: You’re welcome! Happy to help.

Interview 2
Interviewer: Hi there! Thanks for joining us today. We’re excited to hear your feedback on the new Google Single Sign-On (SSO) interface. To start off, can you briefly describe your experience with SSO interfaces in general?
User2: Sure! I’ve used SSO interfaces for various apps and websites. Generally, they simplify the login process by allowing me to use a single set of credentials for multiple platforms, which is really convenient.
Interviewer: Great! Let’s dive into the new Google SSO interface. When you first logged in using this new interface, what was your initial impression?
User2: My initial impression was positive. The interface looks cleaner and more modern compared to the previous version. The login process was straightforward, and it didn’t take long to complete.
Interviewer: That’s good to hear. Did you notice any specific features or changes in this new interface that stood out to you?
User2: Yes, I noticed a couple of things. For one, the new interface has a more streamlined design, which makes it easier to navigate. I also liked the new “Stay Signed In” option; it’s clearer and more accessible now.
Interviewer: How did you find the overall ease of use? Was there anything that you found particularly confusing or difficult?
User2: Overall, the ease of use was quite good. However, I did find the account switching feature a bit confusing at first. I had trouble figuring out how to switch between different accounts without logging out. A bit more guidance or clearer icons might help.
Interviewer: Thank you for pointing that out. Did you encounter any issues or bugs during your experience?
User2: No significant issues, thankfully. Everything seemed to work smoothly. The only minor thing was that the loading time for the initial login screen was a bit longer than I expected.
Interviewer: Noted. Moving on, how do you feel about the overall design and aesthetics of the new SSO interface?
User2: I think the design is quite appealing. It’s clean, minimalistic, and aligns well with Google’s overall design language. The colors and layout are easy on the eyes, which is a plus.
Interviewer: That’s great feedback. Is there anything you would suggest to improve the new Google SSO interface?
User2: Perhaps enhancing the account switching feature with clearer instructions or visual cues would be helpful. Additionally, improving the initial loading speed would enhance the user experience.
Interviewer: Excellent suggestions. Finally, would you say this new SSO interface improves your overall experience compared to the previous version?
User2: Yes, I would say it does. The cleaner design and new features make it more user-friendly and efficient. The minor issues are manageable and don’t significantly detract from the overall positive experience.
Interviewer: Thank you so much for your insights today! Your feedback is invaluable and will help us make further improvements.
User2: You’re welcome! I’m glad I could help.
Interviewer: Have a great day!
User2: You too!

Interview 3
Interviewer: Hi, thanks for joining us today. Can you start by telling me a bit about how you typically use Single Sign-On (SSO) services?
User3: Sure! I use SSO services mostly for accessing various work applications. It simplifies logging in because I don’t have to remember multiple passwords. I mainly use it for tools like email, project management, and document storage.
Interviewer: Great, that helps. Today we’re focusing on the new Google SSO interface. To start, can you describe your first impression of the new interface?
User3: The first thing I noticed was that it looks much cleaner than the previous version. The design is more modern, and everything seems to be more streamlined. It’s easier to find what I need right away.
Interviewer: That's good to hear. Did you find the login process straightforward?
User3: Yes, it was pretty smooth. The new interface makes it clearer which account I’m signing in with. The options for adding or switching accounts are more visible now, which is helpful.
Interviewer: How about the account management features? Were you able to find what you needed easily?
User3: Yes, I found the account management features quite accessible. I liked that I could manage my accounts without having to dig through several menus. The options are consolidated in one place, which is nice.
Interviewer: Did you encounter any difficulties or areas where you felt the experience could be improved?
User3: One small thing I noticed is that the loading time for the account switch seemed a bit longer than I expected. Also, it would be great if there were a quicker way to log out of all accounts at once, especially if you’re using a shared computer.
Interviewer: Thank you for pointing that out. Overall, how would you rate your experience with the new Google SSO interface compared to the old one?
User3: Overall, I’d say it’s a big improvement. The interface is more user-friendly and visually appealing. If the few performance tweaks and additional features you mentioned are addressed, it could be even better.
Interviewer: Thanks for the feedback! Is there anything else you’d like to share about your experience?
User3: Just that I appreciate the effort put into making it more intuitive. It’s a noticeable upgrade, and I think it will make managing my accounts much easier.
Interviewer: Thank you so much for your time and insights. They’re really valuable to us!
User3: You’re welcome! Glad I could help."""
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
