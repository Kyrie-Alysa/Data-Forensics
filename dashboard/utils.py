# utils.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import os

@st.cache_data
def load_data(dataset_name):
    base_dir = os.path.dirname(__file__)  
    path = os.path.join(base_dir, "..", "Data", f"{dataset_name}_posts_tweetnlp.csv")
    path = os.path.abspath(path)
    df = pd.read_csv(path)

    # Filter out empty content
    df = df[df['content'].notna() & (df['content'] != '')]
    df = df[~df['content'].str.match(r"^>>\d+(\s*)$")]

    # For chan4: drop duplicate subpost_id
    if dataset_name == 'chan4' and 'subpost_id' in df.columns:
        df = df.drop_duplicates(subset=['subpost_id'])
    else:
        df = df.drop_duplicates(subset=['content'])

    return df

def merge_with_topics(posts_df, topics_df):
    return posts_df.merge(topics_df[['thread_id', 'tweetnlp_topic']], on='thread_id', how='left')

def plot_label_vs_label(df, x_col, hue_col, percent=False):

    fig, ax = plt.subplots(figsize=(8, 5))

    if percent:
        # Calculate normalized percentage per group
        count_data = (
            df.groupby([x_col, hue_col])
              .size()
              .reset_index(name='count')
        )
        total_per_x = count_data.groupby(x_col)['count'].transform('sum')
        count_data['percent'] = count_data['count'] / total_per_x * 100

        sns.barplot(
            data=count_data,
            x=x_col,
            y='percent',
            hue=hue_col,
            ax=ax
        )
        ax.set_ylabel("Percentage (%)")
    else:
        sns.countplot(data=df, x=x_col, hue=hue_col, ax=ax)
        ax.set_ylabel("Count")

    ax.set_title(f"Distribution of {x_col} against {hue_col}")
    return fig

def filter_and_rank_comments(
    df, 
    emotion=None, 
    hate=None, 
    irony=None, 
    offensive=None,
    sentiment=None,  
    top_n=5
):
    filtered = df.copy()

    if emotion:
        filtered = filtered[filtered['emotion_label'] == emotion]
    if hate:
        filtered = filtered[filtered['hate_label'] == hate]
    if irony:
        filtered = filtered[filtered['irony_label'] == irony]
    if offensive:
        filtered = filtered[filtered['offensive_label'] == offensive]
    if sentiment and 'sentiment_label' in df.columns:
        filtered = filtered[filtered['sentiment_label'] == sentiment]

    # Combine the scores
    score_cols = [col for col in ['emotion_score', 'hate_score', 'irony_score', 'offensive_score', 'sentiment_score'] if col in df.columns]
    filtered['combined_score'] = filtered[score_cols].mean(axis=1)

    # Select the top N comments
    top_comments = filtered.sort_values('combined_score', ascending=False).head(top_n)

    columns_to_return = ['content', 'thread_id'] + score_cols + \
    [col for col in df.columns if col.endswith('_label')]

    # Add topic if present
    if 'tweetnlp_topic' in df.columns:
        columns_to_return.append('tweetnlp_topic')

    return top_comments[columns_to_return]


