import os

import streamlit as st

from layout.header import page_header

def display_podcast(title, image, links):
    st.image(image, use_column_width=True)
    for link, text in links:
        st.markdown(f"[{text}]({link})")

def display_book(title, image, author_link, author_name):
    st.image(image, use_column_width=True)
    st.markdown(f"[By: {author_name}]({author_link})")

page_header("Interests", page_name=os.path.basename(__file__))

# Favorite Podcasts
st.header("My Favorite Podcasts")
st.write("I absolutely love podcasts, many of these episodes are timeless and would highly recommend any of these if you are looking for new content!")

# Podcast Columns
col1, col2, col3 = st.columns(3)

with col1:
    display_podcast(
        title="Reply All",
        image="https://cdn.grapedrop.com/u0e8c2eda803f4757a1488f6bc8b68881/95a0fc568b434eee87c528ec6d2eb039_reply_all.jpg",
        links=[
            ("https://gimletmedia.com/shows/reply-all/n8hw3d/149-3050-feral-hogs", "30-50 Feral Hogs"),
            ("https://gimletmedia.com/shows/reply-all/v4hv68/151-thank-you-for-noticing", "Thank You for Noticing"),
            ("https://gimletmedia.com/shows/reply-all/o2ho6j/56-zardulu", "Zardulu"),
        ]
    )

# ... repeat for other podcasts ...

# My Reading List
st.header("My Reading List")
st.write("These books have been incredibly helpful in my data science journey")

# Book Columns
col1, col2, col3 = st.columns(3)

with col1:
    display_book(
        title="The Effective Engineer",
        image="https://cdn.grapedrop.com/u0e8c2eda803f4757a1488f6bc8b68881/bd11b9acac4a405d9fc27137d5ad6dab_25238425._uy630_sr1200630_.jpeg",
        author_link="https://twitter.com/edmondlau",
        author_name="Edmond Lau"
    )

# ... repeat for other books ...

# You can continue this pattern for the rest of the content
