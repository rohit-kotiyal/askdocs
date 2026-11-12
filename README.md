# AskDocs

Upload your documents. Ask anything. Get answers with sources.

AskDocs is a multi-tenant AI knowledge assistant. Organizations upload their documents, invite team members with role-based access, and ask questions in plain language. Answers come from the organization's own files, with source snippets so every response can be verified.

> Work in progress.

## Planned stack

- Backend: Django, Django REST Framework
- Frontend: React, Tailwind CSS
- Database: PostgreSQL + pgvector
- Background jobs: Celery + Redis
- Auth: JWT, RBAC, multi-tenancy
- AI: Ollama (local LLM), sentence-transformers, RAG
- Deployment: Docker, Kubernetes (kind)

## Status

- [ ] Stage 1: Auth
- [ ] Stage 2: Multi-tenancy and RBAC
- [ ] Stage 3: Document ingestion
- [ ] Stage 4: Embeddings and retrieval
- [ ] Stage 5: RAG answers
- [ ] Stage 6: UI
- [ ] Stage 7: Docker and Kubernetes
- [ ] Stage 8: Polish and demo
