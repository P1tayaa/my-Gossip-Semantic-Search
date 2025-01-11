import feedparser
import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = SCRIPT_DIR + "/../" + os.getenv("DIR_DATA", "data/")

FILENAME = os.getenv("RAW_DATA_NAME", "articles_dataset.csv")
FILENAMETEMP = FILENAME + "_temp"


def fetch_rss_articles(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        articles.append(
            {
                "title": entry.title,
                "link": entry.link,
                "published": entry.published if "published" in entry else None,
                "summary": entry.summary if "summary" in entry else None,
                "source": feed_url,
            }
        )
    return articles


def save_articles_in_chunks(
    articles, temp_filename=DATADIR + FILENAMETEMP, chunk_size=100
):
    if not articles:
        print("No articles to save.")
        return

    for i in range(0, len(articles), chunk_size):
        chunk = articles[i : i + chunk_size]
        df = pd.DataFrame(chunk)
        write_mode = "a" if os.path.exists(temp_filename) else "w"
        header = write_mode == "w"  # Write header only if it's a new file
        df.to_csv(temp_filename, mode=write_mode, header=header, index=False)
        print(f"Saved {len(chunk)} articles to {temp_filename}.")


def save_articles_without_dups(
    temp_filename=DATADIR + FILENAMETEMP,
    final_filename=DATADIR + FILENAME,
):
    if not os.path.exists(temp_filename):
        print(f"Temporary file '{temp_filename}' does not exist.")
        return

    temp_df = pd.read_csv(temp_filename)

    if os.path.exists(final_filename):
        final_df = pd.read_csv(final_filename)
    else:
        final_df = pd.DataFrame(columns=temp_df.columns)

    if "link" not in temp_df.columns or "link" not in final_df.columns:
        raise ValueError("Both datasets must have a 'link' column for deduplication.")

    merged_df = pd.concat([final_df, temp_df]).drop_duplicates(
        subset="link", keep="last"
    )

    merged_df.to_csv(final_filename, index=False)
    print(f"Saved {len(merged_df) - len(final_df)} new articles to {final_filename}.")


def create_dataset():
    rss_feeds = {
        "public.fr": [
            "https://www.public.fr/feed",
            "https://www.public.fr/people/feed",
            "https://www.public.fr/tele/feed",
            "https://www.public.fr/mode/feed",
            "https://www.public.fr/people/familles-royales/feed",
        ],
        "vsd.fr": [
            "https://vsd.fr/actu-people/feed/",
            "https://vsd.fr/tele/feed/",
            "https://vsd.fr/societe/feed/",
            "https://vsd.fr/culture/feed/",
            "https://vsd.fr/loisirs/feed/",
        ],
    }

    all_articles = []
    for site, urls in rss_feeds.items():
        print(f"{urls}\n")
        for url in urls:
            try:
                articles = fetch_rss_articles(url)
                for article in articles:
                    article["site"] = site
                all_articles.extend(articles)

                if len(all_articles) >= 100:
                    save_articles_in_chunks(all_articles[:100])
                    all_articles = all_articles[100:]

            except Exception as e:
                print(f"Error fetching articles from {url}: {e}")

    if all_articles:
        save_articles_in_chunks(all_articles)
    save_articles_without_dups()


if __name__ == "__main__":
    create_dataset()
