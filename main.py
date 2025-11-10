

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from UTILS.api import generate_gemini_response, summerize_voice_content
from UTILS.content import fetch_google_news_rss

# import uvicorn
# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from your React frontend
# In a production environment, you should restrict this to your specific frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def hello():
    return { "data" : "HELLO"}


#Request to /analyze to get analysed content
@app.post("/analyze")
def analyze_news_endpoint(payload: dict):
    user_text = payload.get("text")
    if not user_text:
        raise HTTPException(status_code=400, detail="Text is required in the request body.")

    # Step 1: Fetch related news from Google News
    related_news = fetch_google_news_rss(user_text, max_results=10) # Fetches up to 10 titles and links

    if not related_news:
        # If no news found, still try to analyze the claim with Gemini
        response_data = generate_gemini_response(user_text, [])
    else:
        # Step 2: Pass the user text and related news to Gemini for analysis
        response_data = generate_gemini_response(user_text, related_news)
    
    return response_data


@app.post("/verify_news")
def verify_news_claim(user_input: dict):
    """
    1. Extract keywords from user text using Gemini.
    2. Search Google News using those keywords.
    3. Pass articles to Gemini for final credibility verdict.
    """
    try:
        user_text = user_input.get("text", "")
        if not user_text:
            raise HTTPException(status_code=400, detail="Missing 'text' field.")

        # --- Step 1: Extract Keywords ---
        print("Extracting keywords...")
        keyword_result = summerize_voice_content(user_text)
        keywords = keyword_result.get("keywords", [])

        if not keywords:
            raise HTTPException(status_code=400, detail="No keywords extracted from text.")

        print(f"Extracted keywords: {keywords}")

        # --- Step 2: Fetch Google News for each keyword ---
        all_articles = []
        for keyword in keywords:
            articles = fetch_google_news_rss(keyword, max_results=3)
            all_articles.extend(articles)
            

        if not all_articles:
            raise HTTPException(status_code=404, detail="No news articles found for extracted keywords.")

        print(f"Fetched {len(all_articles)} total articles.")

        # --- Step 3: Generate AI Credibility Report ---
        result = generate_gemini_response(user_text, all_articles)

        return {
            "keywords": keywords,
            "articles_used": len(all_articles),
            "analysis": result
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    



@app.post("/get-audio")
def get_audio_description(audio_path: dict):
    try:
        user_audio = audio_path.get("path", "")
        if not user_audio:
            raise HTTPException(status_code=400, detail="Missing 'path' field.")
        
        # 👇 Safe, lazy import (only happens on request)
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(user_audio, fp16=False)
        return {"text": result["text"]}
    
    except Exception as e:
        print(f"Unexpected error in /get-audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/check-ai")
def check_if_ai(path:dict):
    from transformers import pipeline
    try:
        audio_path = path.get("path", "")
        if not audio_path:
            raise HTTPException(status_code=400, detail="Missing 'text' field.")
        pipe = pipeline("audio-classification", model="abhishtagatya/wav2vec2-base-960h-asv19-deepfake")
        try:
            results = pipe(audio_path)
            print("Prediction Results:", results)

            # The output is typically a list of dictionaries, like:
            # [{'score': 0.999, 'label': 'spoof'}, {'score': 0.001, 'label': 'bonafide'}]

        except Exception as e:
            print(f"An error occurred during prediction: {e}")
            print("Ensure the audio file path is correct and accessible.")

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    pass