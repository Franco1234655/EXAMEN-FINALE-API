from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI()

class Characteristic(BaseModel):
    ram_memory: int
    rom_memory: int

class Phone(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

class PhoneCreate(BaseModel):
    brand: str
    model: str
    characteristics: Characteristic

class PhoneResponse(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

phones_db: List[Phone] = []

@app.get("/health", response_class=PlainTextResponse)
async def health_check():
    """Route de vérification de santé qui retourne 'Ok' en texte brut"""
    return "Ok"

@app.post("/phones", status_code=status.HTTP_201_CREATED, response_model=PhoneResponse)
async def create_phone(phone_data: PhoneCreate):
    """Créer un nouveau téléphone avec un identifiant généré automatiquement"""

    phone_id = str(uuid.uuid4())
    
    new_phone = Phone(
        identifier=phone_id,
        brand=phone_data.brand,
        model=phone_data.model,
        characteristics=phone_data.characteristics
    )
    
   
    phones_db.append(new_phone)
    
    return new_phone

@app.get("/phones", response_model=List[PhoneResponse])
async def get_phones():
    """Récupérer la liste de tous les téléphones"""
    return phones_db

@app.get("/phones/{phone_id}", response_model=PhoneResponse)
async def get_phone(phone_id: str):
    """Récupérer un téléphone spécifique par son identifiant"""
    for phone in phones_db:
        if phone.identifier == phone_id:
            return phone
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Phone with id {phone_id} not found or does not exist"
    )

@app.put("/phones/{phone_id}/characteristics", response_model=PhoneResponse)
async def update_phone_characteristics(phone_id: str, characteristics: Characteristic):
    """BONUS: Mettre à jour les caractéristiques d'un téléphone"""
    for phone in phones_db:
        if phone.identifier == phone_id:
            # Mettre à jour les caractéristiques
            phone.characteristics = characteristics
            return phone
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Phone with id {phone_id} not found or does not exist"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)