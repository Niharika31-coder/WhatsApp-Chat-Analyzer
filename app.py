import streamlit as st
import preproccesor, helper
import matplotlib.pyplot as plt
from pandas.core.interchange.dataframe_protocol import DataFrame

# Title of the app
st.sidebar.title("Whatsapp Chat Analyzer")

# Initialize user_list to avoid NameError
user_list = ["Overall"]  # Default value with "Overall"

# File uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a file", type="txt")

if uploaded_file is not None:
    # Try to read the file as text (UTF-8) and handle potential errors
    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")

        # Preprocess the chat data using the preproccesor function
        df = preproccesor.preprocess(data)

        # Show the dataframe in the app
        st.dataframe(df)

        # Prepare user list
        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")  # Add "Overall" at the start

    except UnicodeDecodeError as e:
        st.error("There was an error decoding the file. Make sure it's a valid text file.")
        st.error(str(e))

    except Exception as e:
        st.error("An unexpected error occurred.")
        st.error(str(e))

# Show the selectbox even if there's no file uploaded yet
selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

if st.sidebar.button("Show Analysis"):

   #stat area
   num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
   col1, col2, col3, col4 = st.columns(4)
   with col1:
        st.header("Total Messages")
        st.title(num_messages)
   with col2:
       st.header("Total Words")
       st.title(words)
   with col3:
       st.header("Media Shared")
       st.title(num_media_messages)
   with col4:
       st.header("Links Shared")
       st.title(num_links)

    #finding the busiest users in the group
   if selected_user == 'Overall':
       st.title('Most Busy User')
       x, new_df = helper.most_busy_users(df)
       fig, ax = plt.subplots()

       col1, col2 = st.columns(2)

       with col1:
           ax.bar(x.index, x.values)
           plt.xticks(rotation = 'vertical')
           st.pyplot(fig)

       with col2:
           st.dataframe(new_df)

    #wordcloud
   st.title("WordCloud")
   df_wc = helper.create_wordcloud(selected_user, df)
   fig,ax = plt.subplots()
   ax.imshow(df_wc)
   st.pyplot(fig)

   #most common words




