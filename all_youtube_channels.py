import os
import json
import csv

BASE_DIR = os.path.join(os.path.dirname(__file__), "users")
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "all_youtube_channels.csv")

def extract_channel_info(channel, user_email):
    """Extracts key fields from a single channel JSON entry."""
    branding = channel.get("brandingSettings", {})
    snippet = channel.get("snippet", {})
    statistics = channel.get("statistics", {})
    image = branding.get("image", {})

    return {
        "user_email": user_email,
        "channel_id": channel.get("id"),
        "title": snippet.get("title") or branding.get("channel", {}).get("title"),
        "description": snippet.get("description") or branding.get("channel", {}).get("description"),
        "country": snippet.get("country") or branding.get("channel", {}).get("country"),
        "channel_url": channel.get("channelUrl"),
        "latest_video_date": channel.get("latestVideoDate"),
        "subscriber_count": statistics.get("subscriberCount"),
        "video_count": statistics.get("videoCount"),
        "view_count": statistics.get("viewCount"),
        "banner_url": image.get("bannerExternalUrl"),
    }

def main():
    rows = []

    for user_folder in os.listdir(BASE_DIR):
        user_path = os.path.join(BASE_DIR, user_folder)
        json_file = os.path.join(user_path, "youtube_subscriptions.json")

        if not os.path.isdir(user_path):
            continue

        if not os.path.exists(json_file):
            continue

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                for channel in data:
                    rows.append(extract_channel_info(channel, user_folder))

        except Exception as e:
            print(f"Error reading {json_file}: {e}")

    # Write CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "user_email", "channel_id", "title", "description", "country",
            "channel_url", "latest_video_date", "subscriber_count",
            "video_count", "view_count", "banner_url"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV created: {OUTPUT_CSV} ({len(rows)} channels)")

if __name__ == "__main__":
    main()
