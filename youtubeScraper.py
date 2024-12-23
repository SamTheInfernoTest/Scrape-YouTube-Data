import pandas as pd
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Initialize YouTube Data API client
def get_youtube_service(api_key):
    return build("youtube", "v3", developerKey=api_key)

# Fetch video details based on search query
def fetch_video_details(youtube, query, max_results=50):
    # Search videos
    search_request = youtube.search().list(
        part="id,snippet",
        q=query,
        type="video",
        maxResults=max_results
    )
    search_response = search_request.execute()

    video_ids = [item["id"]["videoId"] for item in search_response["items"]]

    # Fetch detailed video info
    video_request = youtube.videos().list(
        part="contentDetails,statistics,snippet,topicDetails,recordingDetails",
        id=",".join(video_ids)
    )
    video_response = video_request.execute()

    # Process video details
    video_data = []
    for video in video_response["items"]:
        video_id = video["id"]

        # Fetch captions

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            caption = '\n'.join([s['text'] for s in transcript])
        except Exception as e:
            caption = 'No Caption' 


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
        caption_text = caption

        # Append processed data
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

    return video_data

# Main function
if __name__ == "__main__":
    API_KEY = "AIzaSyC4JyPR12YpIy8Ef1BVgWr-uV9cjnlOSx0"
    youtube = get_youtube_service(API_KEY)

    # Input the genre dynamically
    genre = input("Enter the genre: ").strip()
    print(f"Fetching video details for genre: {genre}")

    # Fetch video details
    video_details = fetch_video_details(youtube, query=genre, max_results=50)

    # Create a DataFrame
    df = pd.DataFrame(video_details)

    # Display the DataFrame
    print(df)

    # Save to a CSV file 
    df.to_csv(f"data/{genre}_videos.csv", index=False)

def getData(genre, number):
    API_KEY = "AIzaSyC4JyPR12YpIy8Ef1BVgWr-uV9cjnlOSx0"
    youtube = get_youtube_service(API_KEY)


    # Fetch video details
    video_details = fetch_video_details(youtube, query=genre, max_results=number)

    # Create a DataFrame
    df = pd.DataFrame(video_details)

    return df