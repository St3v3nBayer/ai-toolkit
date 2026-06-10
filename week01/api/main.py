from fastapi import FastAPI
from pydantic import BaseModel
from week01.models.document import DocumentRecord
from week01.utils.normalizer import normalize_documents

app = FastAPI()

class DocumentBatch(BaseModel):
    documents:  list[dict]

@app.post("/documents")
def mi_endpoint(body: DocumentBatch):
    
    validos, invalidos = normalize_documents(body.documents)

    return { "validos": len(validos), "invalidos": len(invalidos)}

@app.get("/")
def inicio():
    return "Hola Mundo"