from celery import shared_task
from pypdf import PdfReader

from .chunking import split_text
from .models import Chunk, Document


def extract_text(document):
    path = document.file.path
    if path.lower().endswith(".pdf"):
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


@shared_task
def process_document(document_id):
    document = Document.objects.get(id=document_id)
    document.status = Document.Status.PROCESSING
    document.save(update_fields=["status"])
    try:
        text = extract_text(document)
        pieces = split_text(text)
        if not pieces:
            raise ValueError("No text could be extracted from this file.")
        document.chunks.all().delete()
        Chunk.objects.bulk_create(
            Chunk(document=document, organization=document.organization, index=i, content=piece)
            for i, piece in enumerate(pieces)
        )
        document.status = Document.Status.READY
        document.error = ""
    except Exception as exc:
        document.status = Document.Status.FAILED
        document.error = str(exc)
    document.save(update_fields=["status", "error"])