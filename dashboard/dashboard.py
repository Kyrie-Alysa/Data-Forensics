# dashboard.py
import streamlit as st
import pandas as pd
import ast
import os
from utils import (
    load_data,
    merge_with_topics,
    plot_label_vs_label,
    filter_and_rank_comments
)

st.title("TweetNLP Dashboard")

# Choose dataset
dataset_map = {
    "4chan": "chan4",
    "Endchan": "endchan"
}

dataset_display = st.selectbox("Choose a dataset:", list(dataset_map.keys()))
dataset = dataset_map[dataset_display]
df = load_data(dataset)

if 'show_top_5' not in st.session_state:
    st.session_state.show_top_5 = False
if 'top_df' not in st.session_state:
    st.session_state.top_df = None

# Load and merge corresponding thread files with the topics
base_dir = os.path.dirname(__file__)  # gets the path to dashboard/
topic_path = os.path.abspath(os.path.join(base_dir, "..", "Data", f"{dataset}_threads_tweetnlp.csv"))
topics_df = pd.read_csv(topic_path)

# Deduplicate by thread_id
topics_df = topics_df.drop_duplicates(subset=['thread_id'])

# Clean the tweetnlp_topic field if it's a stringified list
if 'tweetnlp_topic' in topics_df.columns:
    topics_df['tweetnlp_topic'] = topics_df['tweetnlp_topic'].apply(
    lambda x: ast.literal_eval(x)[0] if pd.notna(x) and len(ast.literal_eval(x)) > 0 else None
    )

df = merge_with_topics(df, topics_df)

# Display the top 10 rows of the dataset
st.write(f"{dataset_display} dataset:")
st.dataframe(df.head(10))

# Crosstab analysis
st.subheader("Crosstab analysis")
row_label = st.selectbox("Row-label:", [col for col in df.columns if col.endswith('_label')])
col_label = st.selectbox("Column-label:", [col for col in df.columns if col.endswith('_label') and col != row_label])
cross = pd.crosstab(df[row_label], df[col_label], normalize='index') * 100
st.dataframe(cross.style.format("{:.1f}%"))

# Barplot
st.subheader("Display crosstab as barplot")
st.pyplot(plot_label_vs_label(df, col_label, row_label))

# Filter and display top comments with scores and labels
st.subheader("Top 5 comments using filters")

sentiment = st.selectbox("Filter on sentiment:", [None, 'positive', 'neutral', 'negative']) if 'sentiment_label' in df.columns else None
emotion = st.selectbox("Filter on emotion:", [None] + sorted(df['emotion_label'].dropna().unique().tolist()))
hate = st.selectbox("Filter on hate:", [None] + sorted(df['hate_label'].dropna().unique().tolist()))
irony = st.selectbox("Filter on irony:", [None] + sorted(df['irony_label'].dropna().unique().tolist()))
offensive = st.selectbox("Filter on offensiveness", [None] + sorted(df['offensive_label'].dropna().unique().tolist()))

# Display related treads from the top comments
if st.button("Show Top 5 comments"):
    st.session_state.top_df = filter_and_rank_comments(df, emotion, hate, irony, offensive, sentiment)
    st.session_state.show_top_5 = True

if st.session_state.show_top_5 and st.session_state.top_df is not None:
    top_df = st.session_state.top_df

    # ➤ Show top 5 comments
    for _, row in top_df.iterrows():
        st.markdown(f"**Comment:** {row['content']}")

        if 'tweetnlp_topic' in row and pd.notna(row['tweetnlp_topic']):
            st.markdown(f"**Thread Topic:** {row['tweetnlp_topic']}  \n**Thread ID:** {row['thread_id']}")

        label_rows = []
        for label in ['sentiment', 'emotion', 'hate', 'irony', 'offensive']:
            label_col = f"{label}_label"
            score_col = f"{label}_score"
            if label_col in row and score_col in row:
                label_val = row[label_col]
                score_val = round(row[score_col], 2)
                label_rows.append((label.capitalize(), f"{label_val} ({score_val})"))

        st.table(pd.DataFrame(label_rows, columns=["Label Type", "Label (Score)"]))

    # Thread context from thread file
    st.subheader("Show thread context from thread file")

    available_thread_ids = top_df['thread_id'].dropna().unique().tolist()

    if available_thread_ids:
        selected_thread_id = st.selectbox("Choose a thread_id:", available_thread_ids)
        thread_row = topics_df[topics_df['thread_id'] == selected_thread_id]
        if not thread_row.empty:
            st.markdown(f"**Thread ID:** {selected_thread_id}")
            st.markdown(f"**Date & Time:** {thread_row.iloc[0]['time']}")
            st.markdown(f"**Thread Text:** {thread_row.iloc[0]['thread_text']}")
            if 'tweetnlp_topic' in thread_row.columns:
                st.markdown(f"**Topic:** {thread_row.iloc[0]['tweetnlp_topic']}")
        else:
            st.warning("No thread content found for the selected thread_id.")

