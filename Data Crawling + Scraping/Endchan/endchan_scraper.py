import os
from bs4 import BeautifulSoup
import pandas as pd

def scrape_thread_and_posts(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    threads = []
    posts = []

    op_cell = soup.select_one("div.opCell")
    if op_cell:
        thread_id = op_cell.get("id")
        thread_text_tag = op_cell.select_one("div.divMessage")
        thread_text = thread_text_tag.get_text(strip=True) if thread_text_tag else ""
        thread_time = op_cell.select_one("span.labelCreated").get_text(strip=True)

        threads.append({
            "thread_id": thread_id,
            "thread_text": thread_text,
            "time": thread_time
        })

        for post in soup.select("div.postCell"):
            subpost_id = post.get("id")
            post_text_tag = post.select_one("div.divMessage")
            post_text = post_text_tag.get_text(strip=True) if post_text_tag else ""
            post_time = post.select_one("span.labelCreated").get_text(strip=True)

            posts.append({
                "subpost_id": subpost_id,
                "content": post_text,
                "time": post_time,
                "thread_id": thread_id
            })

    return threads, posts


if __name__ == '__main__':
    thread_dir = 'endchan V2/threads_html'
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
    os.makedirs("output", exist_ok=True)
    df_threads.to_csv("endchan V2/output/threads.csv", index=False)
    df_posts.to_csv("endchan V2/output/posts.csv", index=False)
