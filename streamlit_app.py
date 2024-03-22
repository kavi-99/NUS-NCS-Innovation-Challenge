import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
import streamlit as st
import ai_utils

@st.cache_resource
def load_chain():
    """
    Load the chain from the local file system

    Returns:
        chain (Chain): The chain object

    """
    return ai_utils.create_chain()


chain = load_chain()

if 'page' not in st.session_state:
    st.session_state.page = 'chatbot'

# Navigation
st.sidebar.header("Navigate to Page")
# st.sidebar.write("---")
page = st.sidebar.selectbox('',['Chatbot', 'Transport Analysis Report'], format_func=lambda x: "🤖 Chatbot" if x == 'Chatbot' else "📊 Transport Analysis Report")

# Page routing
if page == 'Chatbot':
    
    with st.sidebar:
        st.header("About")
        st.markdown(
            """
            This chatbot is powered by a [LangChain](https://python.langchain.com/docs/get_started/introduction) agent tailored for analyzing and responding to queries related to urban transport systems. It examines traffic conditions, public transport schedules, road safety, and user feedback, employing retrieval-augmented generation (RAG) to delve into both structured and unstructured data. Our primary sources include online discussions, complaint threads, and user-generated content spanning various digital platforms.

            The chatbot aims to distill the community's perceptions, pinpointing prevalent concerns and suggestions. This approach enables a nuanced understanding of the public’s sentiment, facilitating informed discussions and decisions within the urban transport context.
            """
        )

        # st.header("Example Questions")
        # st.markdown("- Which hospitals are in the hospital system?")
        # st.markdown(
        #     """- What is the current wait time at wallace-hamilton hospital?"""
        # )
        # st.markdown(
        #     """- At which hospitals are patients complaining about billing and
        #     insurance issues?"""
        # )
        # st.markdown(
        #     "- What is the average duration in days for closed emergency visits?"
        # )
        # st.markdown(
        #     """- What are patients saying about the nursing staff at
        #     Castaneda-Hardy?"""
        # )
        # st.markdown(
        #     "- What was the total billing amount charged to each payer for 2023?"
        # )


    st.title("Transport and Traffic Chatbot")
    st.info(
        """
        Dive into the pulse of the city! Ask me about the public's views and feelings regarding traffic situations,
        public transportation systems, road safety measures, and overall urban mobility, as shared across social media and public forums.
        
        **Example Questions You Can Ask:**
        
        - "What are the main issues people have with the MRT system?"
        - "What is the public opinion on the newly introduced chimes in public transit?"
        """
    )


    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "output" in message.keys():
                st.markdown(message["output"])

            # if "explanation" in message.keys():
            #     with st.status("How was this generated", state="complete"):
            #         st.info(message["explanation"])

    if prompt := st.chat_input("What do you want to know?"):
        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append({"role": "user", "output": prompt})

        data = {"text": prompt}

        with st.spinner("Searching for an answer..."):
            
            result = chain.invoke(prompt)
            response = "dummy"
                # requests.post(CHATBOT_URL, json=data)
            output_text = result['result']
            # explanation = 
            # if response.status_code == 200:
            #     output_text = response.json()["output"]
            #     explanation = response.json()["intermediate_steps"]

            # else:
            #     output_text = """An error occurred while processing your message.
            #     Please try again or rephrase your message."""
            #     explanation = output_text

        st.chat_message("assistant").markdown(result['result'])
        # st.status("How was this generated?", state="complete").info(explanation)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "output": output_text,
                # "explanation": explanation,
            }
        )
    
elif page == 'Transport Analysis Report':
    # Redirect to the Transport Analysis Report page
    st.session_state.page = 'report'
    st.title("Transport and Traffic Analysis Report")

    with st.sidebar:
        st.header("About")
        st.markdown(
            """
            This report presents an analysis of public sentiment related to transport, based on data scraped from social media and public forums.
            """
        )
            # Data Categorization Explanation
        st.header("Understanding Data Categorization")
        st.write("""
            Our analysis segments the data into two main categories for a clearer understanding of public sentiment:
            
            - **Category 1 (Post Nature)**: This includes the overall nature or intent behind the user's post, categorized into:
                - *Complaint*: Expressions of dissatisfaction or problems.
                - *Suggestion*: Recommendations or ideas for improvement.
                - *Praise*: Positive feedback or approval.
                - *Query*: Questions or requests for information.
                - *Information/News*: Informative content or updates.
                - *Other*: Posts that do not fit into the above categories or are unclear.
            
            - **Category 2 (Subject Matter)**: This pertains to the specific transport-related topic discussed in the post, such as:
                - *Bus Service*: Issues or comments related to bus transportation.
                - *Train Service*: Matters concerning train systems.
                - *Private Transport*: Discussions on personal vehicle use, ride-sharing, etc.
                - *Walk/Cycle*: Topics about pedestrian and cycling infrastructure.
                - *Policy/Regulation*: Comments on transport policies, laws, and governance.
                - *Infrastructure/Facilities/Systems*: Feedback on physical transport infrastructure and facilities.
                - *Other*: Subjects that do not fit into the above categories or are unclear.
        """)

    # Load and display the dataset statistics
    df = pd.read_csv('data/reddit_data_w_summary_categories.csv')

    # Displaying the value counts for each category
    st.subheader("Category 1 Breakdown")
    st.write("See sidebar for more information on categories.")
    col1, col2 = st.columns(2)  # Create two columns for side-by-side display

    with col1:
        st.bar_chart(df["category1"].value_counts())
    with col2:
        st.table(df["category1"].value_counts().reset_index().rename(columns={'index': 'Category', 'category1': 'Count'}))

    st.subheader("Category 2 Breakdown")
    st.write("See sidebar for more information on categories.")
    tab1, tab2, tab3 = st.tabs(["Bar Chart", "Data Table", "Pie Chart"])

    with tab1:
        st.bar_chart(df["category2"].value_counts())

    with tab2:
        st.table(df["category2"].value_counts().reset_index().rename(columns={'index': 'Category', 'category2': 'Count'}))

    with tab3:
        # Increase the figure size for better visibility
        fig, ax = plt.subplots(figsize=(10, 8))  # Adjust size as needed

        # Prepare the data
        labels = df["category2"].value_counts().keys()
        sizes = df["category2"].value_counts()
        explode = [0.05] * len(labels)  # Slightly separate all slices ('explode' them)

        # Create the pie chart with improvements
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%', 
            startangle=140, 
            explode=explode,  # Apply the 'explode' effect
            colors=plt.cm.tab20.colors  # Use a predefined color map for better color distinction
        )

        # Improve label readability
        plt.setp(texts, size='small')  # Decrease label font size if needed or set to 'x-small'
        plt.setp(autotexts, size='medium', weight='bold', color='white')  # Adjust percentage labels

        # Add a legend outside the pie chart, improving label readability
        total = sum(sizes) 
        percentage_labels = [f"{label}: {size / total * 100:.1f}%" for label, size in zip(labels, sizes)]
        ax.legend(wedges, percentage_labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        # Equal aspect ratio ensures that pie is drawn as a circle and improve layout
        ax.axis('equal')
        plt.tight_layout()  

        st.pyplot(fig)

    # Detailed Analysis based on cross_reference mapping
    cross_reference = {'bus service': ['frequency', 'punctuality', 'accessibility', 'affordability', 'quality', 'safety', 'connectivity', 'crowding', 'infrastructure/facilities'],
                  'train service': ['frequency', 'punctuality', 'accessibility', 'affordability', 'quality', 'safety', 'connectivity', 'crowding', 'infrastructure/facilities'],
                  'private transport': ['cost', 'parking', 'safety', 'traffic/congestion', 'connectivity'],
                  'walk/cycle': ['safety', 'infrastructure/facilities'],
                  'policy/regulation': ['enforcement', 'compliance', 'transparency/communication', 'impact'],
                  'other': 'other'
                  }

    st.header("Detailed Analysis of Transport Categories")
    st.write("This section provides an in-depth examination of various transportation categories, such as 'bus service' or 'train service', by breaking them down into specific aspects like 'quality'. These aspects allow for a granular exploration of public sentiment regarding different facets of transport services. The data powering this analysis is sourced from social media platforms and online forums, where discussions are categorized into these themes. This visualization showcases the frequency of discussions or mentions related to each aspect within the chosen category. By examining these metrics, users can gain a clearer understanding of the specific areas of interest and concern within transportation services.")

    cross_reference = {'bus service': ['frequency', 'punctuality', 'accessibility', 'affordability', 'quality', 'safety', 'connectivity', 'crowding', 'infrastructure/facilities'],
                  'train service': ['frequency', 'punctuality', 'accessibility', 'affordability', 'quality', 'safety', 'connectivity', 'crowding', 'infrastructure/facilities'],
                  'private transport': ['cost', 'parking', 'safety', 'traffic/congestion', 'connectivity'],
                  'walk/cycle': ['safety', 'infrastructure/facilities'],
                  'policy/regulation': ['enforcement', 'compliance', 'transparency/communication', 'impact'],
                  'other': 'other'
                  }
    
    selected_category = st.selectbox("Select a service category", list(cross_reference.keys()))

    if isinstance(cross_reference[selected_category], list):
        selected_subcategory = st.selectbox("Select a subcategory", cross_reference[selected_category])
    else:
        selected_subcategory = cross_reference[selected_category]  

    filtered_data = df[(df['category2'] == selected_category) & (df['category3'] == selected_subcategory)]
    st.write("Filtered Data:")
    st.table(filtered_data["category3"].value_counts())

    # Iterate through each main category and its subcategories
    # for main_category, aspects in cross_reference.items():
    #     if aspects != 'other':  # Assuming 'other' doesn't have specific subcategories
    #         st.subheader(f"{main_category} Analysis")

    #         # For each aspect, show the count and possibly visualize
    #         for aspect in aspects:
    #             # Filter data for the current main category and aspect
    #             filtered_df = df.loc[df['category2'] == main_category, 'category3']
    #             counts = filtered_df.value_counts().loc[aspects]

    #             col1, col2 = st.columns(2)
                
    #             with col1:
    #                 # Display the count for the aspect if it exists in the data
    #                 st.write(f"**{aspect}**")
    #                 if aspect in counts:
    #                     st.metric(label=aspect, value=counts[aspect])
    #                 else:
    #                     st.write("No data available")

    #             with col2:
    #                 # Visualize the data for the aspect
    #                 if aspect in counts:
    #                     st.bar_chart(counts)


    # # Display category statistics
    # st.subheader('Post Categories Distribution')
    # st.write(df["category1"].value_counts())
    # st.write(df["category2"].value_counts())

    # # Plotting the distribution of Category 2 (Transport Topics)
    # labels = df["category2"].value_counts().keys()
    # sizes = df["category2"].value_counts()
    # fig, ax = plt.subplots()
    # ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    # st.pyplot(fig)

    # # Detailed Analysis based on Category 2
    # st.subheader('Detailed Analysis Based on Transport Topics')
    # cross_reference = {
    #     'bus service': ['frequency', 'punctuality', 'accessibility', 'affordability', 'quality', 'safety', 'connectivity', 'crowding', 'infrastructure/facilities'],
    #     'train service': ['frequency', 'punctuality', 'accessibility', 'affordability', 'quality', 'safety', 'connectivity', 'crowding', 'infrastructure/facilities'],
    #     'private transport': ['cost', 'parking', 'safety', 'traffic/congestion', 'connectivity'],
    #     'walk/cycle': ['safety', 'infrastructure/facilities'],
    #     'policy/regulation': ['enforcement', 'compliance', 'transparency/communication', 'impact'],
    #     'other': ['other']
    # }

    # # Iterating over each transport topic for detailed sentiment analysis
    # for cat, subcats in cross_reference.items():
    #     if cat != 'other':  # Exclude 'other' from detailed analysis
    #         st.write(f'#### {cat.capitalize()} Topics Analysis:')
    #         for subcat in subcats:
    #             # Assuming there is a column named 'category3' for sub-categories, replace if different
    #             if 'category3' in df.columns:
    #                 subcat_counts = df.loc[df['category2'] == cat, 'category3'].value_counts()
    #                 if subcat in subcat_counts:
    #                     st.write(f"{subcat}: {subcat_counts[subcat]} mentions")
    #                 else:
    #                     st.write(f"{subcat}: No mentions")
    #             else:
    #                 st.write("No detailed category data available.")