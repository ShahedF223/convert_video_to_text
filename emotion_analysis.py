from pytube import YouTube
import moviepy.editor as mp
import speech_recognition as sr

# ==== الخطوة 1: تحميل الفيديو من YouTube ====
def download_youtube_video(url, output_path="video.mp4"):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(filename=output_path)
    print(f"Video downloaded at {output_path}")
    return output_path

# ==== الخطوة 2: استخراج الصوت من الفيديو ====
def extract_audio(video_path, audio_path="audio.wav"):
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    print(f"Audio extracted at {audio_path}")
    return audio_path

# ==== الخطوة 3: تحويل الصوت إلى نص ====
def audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="en-US")  # يمكن تعديل اللغة
    print("Audio converted to text")
    return text

# ==== الخطوة 4: تحليل النص ====
def analyze_text(text, keywords):
    results = {}
    for category, words in keywords.items():
        for word in words:
            if word.lower() in text.lower():
                results[category] = results.get(category, 0) + 1
    
    # تحديد الفئة
    if results:
        dominant_category = max(results, key=results.get)
        print(f"Detected category: {dominant_category} ({results[dominant_category]} matches)")
        return dominant_category, results
    else:
        print("No matching keywords found.")
        return "Neutral", {}

# ==== الخطوة 5: دمج كل الخطوات ====
def main(youtube_url, keywords):
    try:
        video_path = download_youtube_video(youtube_url)
        audio_path = extract_audio(video_path)
        text = audio_to_text(audio_path)
        category, results = analyze_text(text, keywords)
        print(f"Final Analysis: {category}")
        print(f"Keyword Matches: {results}")
    except Exception as e:
        print(f"Error: {e}")

# ==== قاعدة بيانات الكلمات المفتاحية ====
keywords_db = {
    "Happy": ["happy", "joy", "excited", "fun"],
    "Sad": ["sad", "cry", "pain", "tears"],
    "Bullying": ["bully", "harass", "insult", "abuse"]
}

if __name__ == "__main__":
    # أدخل رابط فيديو يوتيوب هنا
    youtube_url = input("Enter YouTube URL: ")
    main(youtube_url, keywords_db)
