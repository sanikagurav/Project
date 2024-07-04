from flask import Flask, render_template, request, redirect, url_for
import os
import speech_processing  # Custom script with conversion and sentiment functions

app = Flask(__name__)

# Set a folder to store uploaded files
UPLOAD_FOLDER = "uploads/"  # Define the upload folder path
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the home page route with form handling
@app.route("/", methods=["GET", "POST"])  # Ensure correct route
def index():
    message = None
    results = None
    
    if request.method == "POST":
        # Ensure the 'audio' key exists in the uploaded files
        if "audio" not in request.files:
            message = "No file part in the request."
        else:
            file = request.files["audio"]  # Retrieve the uploaded file
            if file.filename == "":  # Check if a file was actually uploaded
                message = "No file was selected."
            else:
                # Save the uploaded file to the specified folder
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(file_path)  # Save the file
                
                # Perform speech-to-text conversion
                conversion_result = speech_processing.conversion(file_path, "en-IN")
                
                if conversion_result:
                    text = conversion_result[0]  # Get the extracted text
                    # Perform sentiment analysis
                    sentiment = speech_processing.analyze_sentiment(text)
                    
                    results = {
                        "text": text,
                        "sentiment": sentiment
                    }
                else:
                    message = "Error during audio conversion."

    # Render the template with the message and results
    return render_template("index.html", message=message, results=results)

# Ensure the upload folder exists before running the Flask app
if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])  # Create the upload folder if needed
    
    app.run(debug=True)  # Run Flask with debugging enabled
