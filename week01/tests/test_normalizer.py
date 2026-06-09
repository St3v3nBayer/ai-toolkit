from week01.utils.normalizer import normalize_documents

def test_normalize_separada_validos_e_invalidos():
    docs = [
        {"title": "válido", "content": "contenido válido", "source": "pdf"},
        {"title": "", "content": "x", "source": "excel"}
    ]

    validos, invalidos = normalize_documents(docs)
    assert len(validos) == 1
    assert len(invalidos) == 1