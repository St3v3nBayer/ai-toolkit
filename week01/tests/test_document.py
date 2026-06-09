import pytest
from pydantic import ValidationError
from week01.models.document import DocumentRecord
from datetime import datetime

def test_crear_documento_valido():

    doc = DocumentRecord(
        title = "drilos",
        content = "dassdaffdd",
        source = "pdf"
    )

    assert doc.id is not None
    assert doc.created_at is not None

def test_title_vacio():
    with pytest.raises(ValidationError):
        DocumentRecord(
            title = "",
            content = "contenido válido",
            source = "pdf"
        )

def test_content_muy_corto():
    with pytest.raises(ValidationError):
        DocumentRecord(
            title="Titulo No vacio",
            content="content",
            source="csv"
        )

def test_source_invalido():
    with pytest.raises(ValidationError):
        DocumentRecord(
            title="titulo",
            content="contenido válido",
            source="excel"
        )

def test_tags_sin_duplicados():
    doc = DocumentRecord(
        title="titulo",
        content="contenido válido",
        source="pdf",
        tags=["uno", "dos", "uno"]
    )

    assert doc.tags == ["uno", "dos"]