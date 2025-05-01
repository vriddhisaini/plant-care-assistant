#to incorporate gemini into the project 

import google.generativeai as genai

# Initialize the client with your API key
genai.configure(api_key="api_key")  # Replace "your_api_key" with your actual key

# Use the correct model name format (check Gemini documentation for exact format)
model = genai.GenerativeModel('gemini-1.5-pro')  # Update this if necessary based on documentation

# Test a simple text generation
try:
    # Send a simple prompt to Gemini
    response = model.generate_content(
        "how are you doing"
    )
    
   
    print("Gemini API Response:", response.text)

except Exception as e:
    print(f"An error occurred: {e}")

#sample code:
''' 
# Function to call Gemini API when decision tree can't provide an answer

def call_gemini_api(user_input):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(user_input)
        print("LLM Response:", response.text)  # Debugging response
        return response.text
    except Exception as e:
        return f"An error occurred with Gemini: {str(e)}"


'''