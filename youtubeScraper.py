import os
import pandas as pd
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Initialize YouTube Data API client
def get_youtube_service(api_key):
    return build("youtube", "v3", developerKey=api_key)

# Fetch video captions
def fetch_video_captions(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return '\n'.join([s['text'] for s in transcript])
    except Exception:
        return "No Caption"

# Fetch detailed video information
def fetch_video_details(youtube, query, max_results=50):
    video_data = []
    next_page_token = None
    total_fetched = 0

    while total_fetched < max_results:
        # Fetch search results
        search_request = youtube.search().list(
            part="id,snippet",
            q=query,
            type="video",
            maxResults=min(50, max_results - total_fetched),
            pageToken=next_page_token
        )
        search_response = search_request.execute()

        video_ids = [item["id"]["videoId"] for item in search_response["items"]]

        if not video_ids:
            break  # Stop if no more videos are found

        # Fetch detailed information for video IDs
        video_request = youtube.videos().list(
            part="contentDetails,statistics,snippet,topicDetails,recordingDetails",
            id=",".join(video_ids)
        )
        video_response = video_request.execute()

        for video in video_response["items"]:
            video_id = video["id"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            title = video["snippet"]["title"]
            description = video["snippet"].get("description", "No Description")
            channel_title = video["snippet"]["channelTitle"]
            keyword_tags = ", ".join(video["snippet"].get("tags", []))  # Join tags into a string
            category_id = video["snippet"].get("categoryId", "Unknown")
            topics = ", ".join(video.get("topicDetails", {}).get("topicCategories", []))
            published_at = video["snippet"]["publishedAt"]
            duration = video["contentDetails"]["duration"]  # ISO 8601 duration format
            view_count = int(video["statistics"].get("viewCount", 0))
            comment_count = int(video["statistics"].get("commentCount", 0))
            captions_available = "captionTracks" in video.get("contentDetails", {})
            location = video.get("recordingDetails", {}).get("locationDescription", "No Location")
            caption_text = fetch_video_captions(video_id)

            # Append video data
            video_data.append({
                "Video URL": video_url,
                "Title": title,
                "Description": description,
                "Channel Title": channel_title,
                "Keyword Tags": keyword_tags,
                "YouTube Video Category": category_id,
                "Topic Details": topics,
                "Video Published at": published_at,
                "Video Duration": duration,
                "View Count": view_count,
                "Comment Count": comment_count,
                "Captions Available": captions_available,
                "Caption Text": caption_text,
                "Location of Recording": location
            })

        # Update pagination details
        next_page_token = search_response.get("nextPageToken")
        total_fetched += len(video_ids)

        if not next_page_token:
            break

    return video_data

# Main function
def getData(genre, number):
    API_KEY = "AIzaSyC4JyPR12YpIy8Ef1BVgWr-uV9cjnlOSx0"
    youtube = get_youtube_service(API_KEY)

    # Fetch video details
    video_details = fetch_video_details(youtube, query=genre, max_results=number)

    # Create a DataFrame
    df = pd.DataFrame(video_details)
    return df

if __name__ == "__main__":
    # Input the genre dynamically
    genre = input("Enter the genre: ").strip()
    number = int(input("Enter the number of videos to fetch (up to 500): ").strip())

    print(f"Fetching video details for genre: {genre} ({number} videos)")

    # Fetch video details and save as CSV
    df = getData(genre, number)

    # Display DataFrame
    print(df)

    # Save results to CSV
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{genre}_videos.csv")
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
