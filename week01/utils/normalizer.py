from week01.models.document import DocumentRecord
from pydantic import ValidationError



def normalize_documents(documents: list[dict]) -> tuple[list[DocumentRecord], list[dict]]:
    invalidos = []
    validos = []
   
    for document in documents:
        try:
            doc = DocumentRecord(**document)
            validos.append(doc)
        except ValidationError as e:
            invalidos.append({"data": document, "error": str(e)})

    return validos, invalidos           
    
