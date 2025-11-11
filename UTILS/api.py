from fastapi import HTTPException
import requests
import json
import time
from UTILS.content import get_content_from_link

#API KEY DECLARATION
# GEMINI_API_KEY = "AIzaSyDH06vyJHu3GpKWg2Hqjp-on0vD4mjjI7o"
GEMINI_API_KEY = "AIzaSyAcqTRiQqtEORsL8o6bppPm6CHlRuq5uFA"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"

# #Function definition
# def generate_gemini_response(user_text, news_articles):
#     api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"
    
#     # Construct a detailed prompt
#     articles_context = "\n".join([
#         f"Source: {article['source']}\nTitle: {article['title']}\nExcerpt: {get_content_from_link(article['link'])}"
#         for article in news_articles
#     ])

#     system_prompt = """You are an AI-Powered Misinformation Detector. Your goal is to provide an evidence-based, non-accusatory verdict on the credibility of a news claim.

#         **Your Task (All in one step):**
#         1. **Analyze the Claim:** First, perform a detailed analysis of the user's claim. Extract key entities, keywords, and the overall sentiment or emotional tone.
#         2. **Evaluate External Sources:** Next, analyze the provided list of external news articles. For each article, determine its stance relative to the user's claim, classifying it as 'Supports', 'Conflicts', or 'Neutral'. Pay close attention to the source's reputation, as articles from highly credible sources carry more weight.
#         3. **Calculate Credibility Score:** Based on a neutral starting score of 50, adjust the score using the following logic, ensuring the final score is clamped between 0 and 100:
#         - For every credible source that **supports** the claim, increase the score by 5 points.
#         - For every credible source that **conflicts** with the claim, decrease the score by 10 points.
#         - For every credible source that is **neutral**, do not adjust the score, but recognize that this indicates a lack of strong corroboration.
#         - If the user's original claim contains highly sensational or emotionally charged language, apply a penalty of 10 points to the final score.
#         4. **Determine Verdict and Reasons:** Map the final score to a clear verdict (High Likelihood of Misinformation, Conflicting or Uncorroborated Claims, or Likely Credible). Provide three distinct, evidence-based reasons for your verdict, drawing from your analysis of the sources.Provide atleast 5 reasons
#         5. **State the 'What-If':** Conclude the analysis by providing a specific, verifiable type of evidence that would be needed to change the verdict.
#         6. **Generate a Visual Data Structure:** Create a 'lineage_graph' JSON object that represents the user's claim and its relationship to the top 4 most relevant articles. Use 'Supports' or 'Conflicts' to describe the link type.
#         7.Also include how did you calculated the confidence score
        
#         **Strict JSON Output:**
#         Provide the entire response as a single JSON object. The structure must be exactly as follows. Do not include any other text or markdown outside this JSON object.

#         {{
#             "verdict": "string",
#             "confidence_score": "number",
#             "reasons": ["string", "string", "string"],
#             "what_would_change": "string",
#             "lineage_graph": {
#             "claim": "string",
#             "connections": [
#                 {
#                     "source": "String",
#                     "url" : "url"
#                     "title": "String",
#                     "link_type": "Supports or Contradict"
#                 },
#                 {
#                     "source": "String",
#                     "url" : "url"
#                     "title": "String",
#                     "link_type": "Supports or Contradict"
#                 },
                
#                 {
#                     "source": "String",
#                     "url" : "url"
#                     "title": "String",
#                     "link_type": "Supports or Contradict"
#                 }
#                 .......
#             ]
#         },
#         "confidence_score_calculation": "String"

#         }}
# """

#     user_query = f"""
#       Analyze the following news text:
#       "{user_text}"

#       Here is the list of news articles I have found:
#       {articles_context}
#     """
    
#     payload = {
#         "contents": [{"parts": [{"text": user_query}]}],
#         "systemInstruction": {"parts": [{"text": system_prompt}]},
#         "generationConfig": {"responseMimeType": "application/json"},
#     }

#     try:
#         response = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"})
#         response.raise_for_status()
        
#         # Parse the JSON string from the response
#         json_string = response.json()['candidates'][0]['content']['parts'][0]['text']
#         return json.loads(json_string)
        
#     except requests.exceptions.RequestException as e:
#         print(f"Error calling Gemini API: {e}")
#         raise HTTPException(status_code=500, detail="Error communicating with AI service.")
#     except (KeyError, json.JSONDecodeError) as e:
#         print(f"Error parsing Gemini response: {e}")
#         print(f"Raw Gemini response was: {response.text}")
#         raise HTTPException(status_code=500, detail="Invalid response from AI service.")




# def summerize_voice_content(user_text):
#    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"

#    system_prompt = """
#         You are an ai agent, What you will do is:
#          Read the given text carefully.

#         Extract the most important keywords, entities, or claims (people, dates, events, places, organizations, numbers, etc.).

#         Output the keywords as json with a list of keyword .
#    """
#    user_query = f"""
#           Analyse the following text: 
#           "{user_text}"
#    """
#    payload = {
#         "contents": [{"parts": [{"text": user_query}]}],
#         "systemInstruction": {"parts": [{"text": system_prompt}]},
#         "generationConfig": {"responseMimeType": "application/json"},
#     }

#    try:
#         response = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"})
#         response.raise_for_status()
        
#         # Parse the JSON string from the response
       
#         json_string = response.json()['candidates'][0]['content']['parts'][0]['text']
#         return json.loads(json_string)
        
#    except requests.exceptions.RequestException as e:
#         print(f"Error calling Gemini API: {e}")
#         raise HTTPException(status_code=500, detail="Error communicating with AI service.")
#    except (KeyError, json.JSONDecodeError) as e:
#         print(f"Error parsing Gemini response: {e}")
#         print(f"Raw Gemini response was: {response.text}")
#         raise HTTPException(status_code=500, detail="Invalid response from AI service.")
   
# if __name__ == "__main__":
#     user_inp = """brothers and sisters, wake up! Something terrible is happening behind our backs. And if we stay silent, our democracy is dead. The elections you are seeing on TV, they are not real. The votes we are casting are not going where we think. Yes, the EVM machines are being hacked. Do you think I am making this up? Then explain this. How is it possible that in so many polling booths, one candidate gets thousands of votes while the others get zero? Zero has that ever happened in history. In Uttar Pradesh, in Madhya Pradesh, in Delhi, there are reports already. My friend's uncle was a polling agent in Ghaziabad. He saw with his own eyes that when someone pressed button two, the light blinked on button four again and again. And when they complained, the officials just smiled and said, system error don't worry. System error on election day? Listen carefully. This is not just a glitch. This is a conspiracy. The machines are being pre-loaded. The chips inside are programmed. And who controls the chips? Foreign companies. Yes, imported parts are used in our own election machines. Why would a self-respecting democracy import chips for elections? Think. People will tell you, EVMS cannot be hacked. Ha ha ha. Do you believe that? In today's world, even space satellites are hacked, but our machines are somehow magical and untouchable. NO exclamation mark, exclamation mark, exclamation mark. They can be hacked. They are being hacked. Do you know why exit polls always look so confident because the result is already decided? They know which side the EVM will tilt. And then the media sells you the illusion that the people chose it. Did you choose it? Did your family choose it? Or is it being forced on us? One more thing. Why are CCTV cameras in counting centers often malfunctioning at the crucial moment? Why do power cuts happen exactly when results are being uploaded? Is it all coincidence? No. This is a script being run step by step. And if you still don't believe me, ask yourself, why is the ruling party so relaxed, so smug, even when people on the ground are angry? Because they know the game is fixed. They don't fear the voter. They control the machine. We have fought for independence with our blood. Our freedom fighters gave their lives. And now, with just a few microchips, it is being stolen from us. If we lose this battle, then we are slaves again. But this time, slaves inside our own country. Please don't ignore this. Share this message now. Demand paper ballots. Demand verification. Stand outside polling booths and watch the machines. Do not let them cheat us in silence. If you stay quiet today, tomorrow, you will wake up in a country where your vote means nothing. Nothing. Is that the future you want for your children? Act now. Speak out. Share this to every group you are in. Let the truth spread faster than their lies. Only we can save our democracy."""
#     output = summerize_voice_content(user_inp)
#     print(output)


HEADERS = {"Content-Type": "application/json"}

def safe_post_with_backoff(url, payload, headers, retries=5):
    """Make a POST request with exponential backoff for rate-limit handling."""
    for attempt in range(retries):
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 429:
            wait = 2 ** attempt
            print(f"[Gemini] Rate limit hit (429). Retrying in {wait} seconds...")
            time.sleep(wait)
            continue
        elif response.status_code >= 500:
            wait = 2 ** attempt
            print(f"[Gemini] Server error {response.status_code}. Retrying in {wait} seconds...")
            time.sleep(wait)
            continue
        else:
            # Success or client error
            response.raise_for_status()
            return response

    raise HTTPException(status_code=429, detail="Gemini API rate limit exceeded after multiple retries.")


# ==============================
# FUNCTION 1 — GENERATE FACT CHECK ANALYSIS
# ==============================

def generate_gemini_response(user_text, news_articles):
    api_url = GEMINI_URL
    
    # Build detailed context
    articles_context = "\n".join([
        f"Source: {article['source']}\nTitle: {article['title']}\nExcerpt: {get_content_from_link(article['link'])}"
        for article in news_articles
    ])

    system_prompt = """You are an AI-Powered Misinformation Detector. Your goal is to provide an evidence-based, non-accusatory verdict on the credibility of a news claim.

        **Your Task (All in one step):**
        1. **Analyze the Claim:** First, perform a detailed analysis of the user's claim. Extract key entities, keywords, and the overall sentiment or emotional tone.
        2. **Evaluate External Sources:** Next, analyze the provided list of external news articles. For each article, determine its stance relative to the user's claim, classifying it as 'Supports', 'Conflicts', or 'Neutral'. Pay close attention to the source's reputation, as articles from highly credible sources carry more weight.
        3. **Calculate Credibility Score:** Based on a neutral starting score of 50, adjust the score using the following logic, ensuring the final score is clamped between 0 and 100:
        - For every credible source that **supports** the claim, increase the score by 5 points.
        - For every credible source that **conflicts** with the claim, decrease the score by 10 points.
        - For every credible source that is **neutral**, do not adjust the score, but recognize that this indicates a lack of strong corroboration.
        - If the user's original claim contains highly sensational or emotionally charged language, apply a penalty of 10 points to the final score.
        4. **Determine Verdict and Reasons:** Map the final score to a clear verdict (High Likelihood of Misinformation, Conflicting or Uncorroborated Claims, or Likely Credible). Provide three distinct, evidence-based reasons for your verdict, drawing from your analysis of the sources.Provide atleast 5 reasons
        5. **State the 'What-If':** Conclude the analysis by providing a specific, verifiable type of evidence that would be needed to change the verdict.
        6. **Generate a Visual Data Structure:** Create a 'lineage_graph' JSON object that represents the user's claim and its relationship to the top 4 most relevant articles. Use 'Supports' or 'Conflicts' to describe the link type.
        7.Also include how did you calculated the confidence score. Cap the score between 0 to 100.
        
        **Strict JSON Output:**
        Provide the entire response as a single JSON object. The structure must be exactly as follows. Do not include any other text or markdown outside this JSON object.
        For the image add the image of the incident that you got from that website. The image cannot be null.
        and it should be a valid image, and related to the content.
        {{
            "verdict": ["AI GENERATED", "NOT AI GENERATED"],
            "confidence_score": "number",
            "reasons": ["string", "string", "string"],
            "what_would_change": "string",
            "lineage_graph": {
            "claim": "string",
            "connections": [
                {
                    "source": "String",
                    "url" : "url"
                    "title": "String",
                    "image" : "url",
                    "link_type": "Supports or Contradict"
                },
                {
                    "source": "String",
                    "url" : "url"
                    "title": "String",
                    "image" : "url",
                    "link_type": "Supports or Contradict"
                },
                
                {
                    "source": "String",
                    "url" : "url"
                    "title": "String",
                    "image" : "url",
                    "link_type": "Supports or Contradict"
                }
                .......
            ]
        },
        "confidence_score_calculation": "String"

        }}
"""


    user_query = f"""
      Analyze the following claim:
      "{user_text}"

      Here are related news articles:
      {articles_context}
    """

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"responseMimeType": "application/json"},
    }

    try:
        response = safe_post_with_backoff(api_url, payload, HEADERS)

        json_string = response.json()['candidates'][0]['content']['parts'][0]['text']
        return json.loads(json_string)

    except requests.exceptions.RequestException as e:
        print(f"[Gemini Error] {e}")
        raise HTTPException(status_code=500, detail="Error communicating with AI service.")
    except (KeyError, json.JSONDecodeError) as e:
        print(f"[Gemini Parse Error] {e}")
        print(f"Raw response: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid response from AI service.")


# ==============================
# FUNCTION 2 — KEYWORD EXTRACTION
# ==============================

def summerize_voice_content(user_text):
    api_url = GEMINI_URL

    system_prompt = """
        You are an AI agent.
        Read the given text carefully.
        Extract the most important keywords, entities, or claims (people, dates, events, places, organizations, numbers, etc.).
        Return output as valid JSON:
        { "keywords": ["keyword1", "keyword2", "keyword3"] }
    """

    user_query = f"""
        Analyse the following text: 
        "{user_text}"
    """

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"responseMimeType": "application/json"},
    }

    try:
        response = safe_post_with_backoff(api_url, payload, HEADERS)
        json_string = response.json()['candidates'][0]['content']['parts'][0]['text']
        return json.loads(json_string)

    except requests.exceptions.RequestException as e:
        print(f"[Gemini Error] {e}")
        raise HTTPException(status_code=500, detail="Error communicating with AI service.")
    except (KeyError, json.JSONDecodeError) as e:
        print(f"[Gemini Parse Error] {e}")
        print(f"Raw response: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid response from AI service.")