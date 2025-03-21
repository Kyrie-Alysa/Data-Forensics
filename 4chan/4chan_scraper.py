import os
from bs4 import BeautifulSoup
import pandas as pd

def scrape_thread_and_posts(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    threads = []
    posts = []

    # Grab the whole thread
    thread_div = soup.select_one("div.thread")
    if not thread_div:
        return threads, posts

    # Extract OP post
    op_post = thread_div.select_one("div.post.op")
    if op_post:
        thread_id = op_post.get("id")  # e.g., p501051364
        content_tag = op_post.select_one("blockquote.postMessage")
        time_tag = op_post.select_one("span.dateTime")

        thread_text = content_tag.get_text(strip=True) if content_tag else ""
        thread_time = time_tag.get_text(strip=True) if time_tag else ""

        threads.append({
            "thread_id": thread_id,
            "thread_text": thread_text,
            "time": thread_time
        })

    # Extract replies
    for reply in thread_div.select("div.post.reply"):
        post_id = reply.get("id")  # e.g., p501051405
        content_tag = reply.select_one("blockquote.postMessage")
        time_tag = reply.select_one("span.dateTime")

        post_text = content_tag.get_text(strip=True) if content_tag else ""
        post_time = time_tag.get_text(strip=True) if time_tag else ""

        posts.append({
            "subpost_id": post_id,
            "content": post_text,
            "time": post_time,
            "thread_id": thread_id
        })

    return threads, posts

if __name__ == '__main__':
    thread_dir = '4chan/threads_html'
    all_threads = []
    all_posts = []

    for filename in os.listdir(thread_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(thread_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()

            threads, posts = scrape_thread_and_posts(html_content)
            all_threads.extend(threads)
            all_posts.extend(posts)

    # Create DataFrames
    df_threads = pd.DataFrame(all_threads)
    df_posts = pd.DataFrame(all_posts)

    # Print summaries
    print("Total threads scraped:", len(df_threads))
    print("Total posts scraped:", len(df_posts))

    # Save results
    os.makedirs("4chan/output", exist_ok=True)
    df_threads.to_csv("4chan/output/threads.csv", index=False)
    df_posts.to_csv("4chan/output/posts.csv", index=False)
