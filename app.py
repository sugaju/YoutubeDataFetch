from dotenv import load_dotenv

# .env ファイルの読み込み
load_dotenv()

from flask import Flask, render_template, redirect, url_for
import os
import googleapiclient.discovery

app = Flask(__name__)

# YouTube APIキーを設定
api_key = os.environ.get("YOUTUBE_API_KEY")

if not api_key:
    raise ValueError("YouTube APIキーが設定されていません。環境変数 YOUTUBE_API_KEY を設定してください。")

search_titles = ["Python", "プログラミング", "初心者", "入門"]  # ここを検索したいタイトルに変更

@app.route('/')
def index():
    all_videos = []
    for title in search_titles:
        result = search_videos_by_title(title)
        all_videos.extend(result)
    return render_template('index.html', videos=all_videos)

def search_videos_by_title(title):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # YouTube Data APIのsearch.listメソッドを使用して動画を検索
    request = youtube.search().list(
        q=title,
        part="snippet",
        type="video",
        maxResults=50, # 取得する動画の数を指定
        relevanceLanguage="ja"  # 日本語の動画を優先
    )

    response = request.execute()

    # 結果から動画の情報を取得
    videos = []
    for item in response["items"]:
        video = {
            "title": item["snippet"]["title"],
            "video_id": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["default"]["url"]
        }
        videos.append(video)

    return videos

@app.route('/watch/<video_id>')
def watch(video_id):
    # /watch/<video_id>にアクセスされたときの処理
    youtube_url = f'https://www.youtube.com/watch?v={video_id}'
    return redirect(youtube_url)

if __name__ == '__main__':
    app.run(debug=True)

