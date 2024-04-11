from lib2to3.fixes.fix_filter import FixFilter
from fastapi import FastAPI
import os
import firebase_admin
from firebase_admin import credentials, firestore


app = FastAPI()


cred = credentials.Certificate("kpitapp-9ee54-firebase-adminsdk-65o73-3226aa7fd1.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.get("/")
async def root():
    """ doc_ref = db.collection("AliadosEngaged").document('prueba')
    doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815}) """
    return {"message": "Hola mundo!"}

project_id = os.environ.get("PROJECT_ID")

@app.get("/api/engaged/codigo/")
async def codigo(q:str):
    if len(q) > 3:
        docs = db.collection("AliadosEngaged").stream()
        for doc in docs:            
            collections = db.collection("AliadosEngaged").document(doc.id).collections()
            for collection in collections:
                for doc in collection.stream():
                    primer_apellido = doc.get('primerApellido').lower()
                    print(primer_apellido)                    
                    if q.lower() in primer_apellido:
                        print(f"{doc.id} => {doc.to_dict()}")
                        # Si encontramos la subcadena, podemos salir de los bucles y devolver True                        
                        return True
                    else:
                        # Si el bucle interno termina sin encontrar la subcadena, continuamos con el siguiente documento
                        continue
                    # Si encontramos la subcadena, salimos del bucle externo y devolvemos True
            
        return False
    else:
        # Si no se encuentra la subcadena en ningún documento, devolvemos False
        return False

       

