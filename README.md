README: Sentiment Analysis on Imageboard Forums
==============================

Authors: Kyrie-Alysa van IJsselmuide & Kim van Kemenade <br>
Assignment: Data Forensics - Scientific Report  <br>
Goal: Analyze the sentiment and emotional tone of posts on politically incorrect boards of 4chan (surface web) and Endchan (dark web) <br>
Submission: forensics-group3.zip <br>

File Structure Overview:
------------------------------

1. dashboard/
   
   ├── dashboard.py            - Streamlit app for exploring and visualizing sentiment data.
   
   └── utils.py                - Helper functions used by the dashboard.

3. Data/
   
   ├── chan4_posts_tweetnlp.csv         - Preprocessed TweetNLP output for 4chan posts.
   
   ├── chan4_threads_tweetnlp.csv       - Preprocessed TweetNLP output for 4chan threads.
   
   ├── endchan_posts_tweetnlp.csv       - Preprocessed TweetNLP output for Endchan posts.
   
   └── endchan_threads_tweetnlp.csv     - Preprocessed TweetNLP output for Endchan threads.

5. Data Crawling + Scraping/
   
   ├── 4chan/                 - Raw data and scraping scripts for 4chan.
   
   └── Endchan/               - Raw data and scraping scripts for Endchan.

7. DataExploration.ipynb      - Jupyter notebook for exploratory data analysis and visualization.

8. TweetNLP.ipynb             - Notebook applying TweetNLP models for sentiment, emotion, hate speech, irony, and offensive classification.

9. access_token.txt           - Token required for protected dataset access, required for running the DARKBert model within the DataExploration.ipynb notebook.

10. requirements.txt           - List of required Python packages for running the project.

11. Report.pdf                 - Scientific Report

12. README.md                  - This instruction file.

------------------------------
Packages Overview:
------------------------------

- Python 3.10.16
- beautifulsoup4     4.13.4
- bertopic           0.17.0
- fake_useragent     2.2.0
- matplotlib         3.10.3
- nltk               3.9.1
- numpy              2.2.6
- pandas             2.2.3
- playwright         1.52.0
- requests           2.32.3
- scikit-learn       1.6.1
- seaborn            0.13.2
- spacy              3.8.5
- streamlit          1.45.1
- tqdm               4.67.1
- transformers       4.51.3
- tweetnlp           0.4.5

------------------------------
Run Instructions:
------------------------------

1. Set up the environment:
   - Install required packages using: `pip install -r requirements.txt`

2. To run the Streamlit dashboard:
   - Navigate to the project root directory in your terminal.
   - Run the app with: `streamlit run dashboard/dashboard.py`
   - Or access the app directly via: https://dataforensics-3-sentimentforums.streamlit.app/ 

3. To run sentiment analysis or preprocessing:
   - Open `TweetNLP.ipynb` to apply the TweetNLP models
   - Open `DataExploration.ipynb` to explore the initial data exploration and modeling, and visualize results

------------------------------
Notes:
------------------------------
- If the streamlit app is inaccesible due to inactivity, you can run it locally as described above.
- Ensure you have the necessary access token in `access_token.txt` for running the DARKBert model.

