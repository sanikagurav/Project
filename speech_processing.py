import speech_recognition as sr
from textblob import TextBlob

# Function to convert audio to text
def conversion(file_path, lang="en-IN"):
    r = sr.Recognizer()
    result = []
    
    try:
        with sr.AudioFile(file_path) as source:
            print("Fetching file")
            audio = r.record(source)  # Use record to capture the entire audio file
            print("Converting audio to text....")
            text = r.recognize_google(audio, language=lang)
            result.append(text)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return result

# Function to perform sentiment analysis and return a label
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment

# Test the function and perform sentiment analysis
if __name__ == "__main__":
    result = conversion("test.wav", "en-IN")
    
    if result:  # If there is text to analyze
        text = result[0]
        print("Text extracted:", text)
        
        # Perform sentiment analysis and get the label
        sentiment = analyze_sentiment(text)
        
        print("Sentiment:", sentiment)  # Displays Positive, Negative, or Neutral
    else:
        print("No text extracted for sentiment analysis.")
