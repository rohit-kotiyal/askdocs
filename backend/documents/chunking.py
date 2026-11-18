def split_text(text, size=800, overlap=100):
    text = " ".join(text.split())
    chunks = []
    start = 0

    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap

    return chunks