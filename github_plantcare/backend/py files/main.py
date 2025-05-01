from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Plant, Category, CareTip, PlantName, PlantCategory
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import google.generativeai as genai
import re 

genai.configure(api_key="api_key") 



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ---------------------- PLANTS ----------------------
@app.get("/plants")
def get_plants(db: Session = Depends(get_db)):
    try:
        return db.query(Plant).all()
    except Exception as e:
        return {"detail": f"Error fetching plants: {str(e)}"}

@app.get("/plants/{plant_id}")
def get_plant(plant_id: str, db: Session = Depends(get_db)):
    try:
        plant = db.query(Plant).filter(Plant.plant_id == plant_id).first()
        if plant:
            return plant
        return {"error": "Plant not found"}
    except Exception as e:
        return {"detail": f"Error fetching plant: {str(e)}"}

# ---------------------- CATEGORIES ----------------------
@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    try:
        return db.query(Category).all()
    except Exception as e:
        return {"detail": f"Error fetching categories: {str(e)}"}

# ---------------------- CARE TIPS ----------------------
@app.get("/care_tips/{plant_id}")
def get_care_tips(plant_id: str, db: Session = Depends(get_db)):
    try:
        care_tip = db.query(CareTip).filter(CareTip.plant_id == plant_id).first()
        if care_tip:
            return care_tip
        return {"error": "Care tips not found"}
    except Exception as e:
        return {"detail": f"Error fetching care tips: {str(e)}"}

# ---------------------- PLANT-CATEGORY RELATIONSHIP ----------------------
@app.get("/plant_categories")
def get_plant_categories(db: Session = Depends(get_db)):
    try:
        return db.query(PlantCategory).all()
    except Exception as e:
        return {"detail": f"Error fetching plant-category links: {str(e)}"}

# ---------------------- CHATBOT ----------------------
class ChatRequest(BaseModel):
    user_message: str

# Function to call Gemini API when decision tree can't provide an answer
def call_gemini_api(user_input):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(user_input)
        print("LLM Response:", response.text)  
        return response.text
    except Exception as e:
        return f"An error occurred with Gemini: {str(e)}"


@app.post("/chat")
def chat_bot(request: ChatRequest, db: Session = Depends(get_db)):
    message = request.user_message.lower().strip()
    words = re.findall(r'\b\w+\b', message)  # Splits properly into words

    if message.startswith("gemini: "):
     query = message[len("gemini "):]  # remove "gemini " part
     gemini_response = call_gemini_api(query)
     return {"response": f"*LLM generated response:*<br>{gemini_response}"}

    # Greeting responses
    if any(word in words for word in ["hi", "hello", "hey"]):
        return {"response": "Hi there! How can I help your plant today?"}

    # How are you response
    elif "how are you" in message:
        return {"response": "I'm great! How can I help your plant?"}

    # Farewell responses
    elif any(word in words for word in ["bye", "goodbye", "see", "okay", "huh"]):
        return {"response": "Goodbye! Take care and happy planting!"}

    # Care-related responses
    elif any(word in words for word in ["care", "water", "sunlight", "soil", "humidity", "temperature"]):
        # Identifying plant from DB
        plant_names = db.query(PlantName).all()
        matched_plant = None
        for pname in plant_names:
            if pname.name.lower() in message:
                matched_plant = pname
                break

        if matched_plant is None:
            # LLM fallback
            gemini_response = call_gemini_api(message)
            return {"response": f"*LLM generated response:*<br>{gemini_response}"}

        # Fetch care tips from DB
        plant_id = matched_plant.plant_id
        care = db.query(CareTip).filter(CareTip.plant_id == plant_id).first()

        if not care:
            return {"response": f"*Care information for {matched_plant.name} is not available.*"}

        # Handle specific care-related requests
        if "water" in words:
            return {"response": f"*Watering info for {matched_plant.name}:*\n{care.watering}"}
        elif "sunlight" in words:
            return {"response": f"*Sunlight info for {matched_plant.name}:*\n{care.sunlight}"}
        elif "soil" in words:
            return {"response": f"*Soil info for {matched_plant.name}:*\n{care.soil}"}
        elif "temperature" in words or "temp" in words:
            return {"response": f"*Temperature info for {matched_plant.name}:*\n{care.temp}"}
        elif "humidity" in words:
            return {"response": f"*Humidity info for {matched_plant.name}:*\n{care.humidity}"}
        else:
            return {
                "response": f"""*Care for {matched_plant.name}:*<br>
*1. Water:* {care.watering}<br>
*2. Sunlight:* {care.sunlight}<br>
*3. Soil:* {care.soil}<br>
*4. Temperature:* {care.temp}<br>
*5. Humidity:* {care.humidity}<br>
*6. Common Issues:* {care.common_issues}<br>"""
            }

    else:
        gemini_response = call_gemini_api(message)
        return {"response": f"*LLM generated response:*<br>{gemini_response}"}
    



#uvicorn main:app --reload -> to run fastapi on local host 
