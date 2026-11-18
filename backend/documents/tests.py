import tempfile

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase

from accounts.models import Organization, User

from .models import Document
from .tasks import process_document

TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class DocumentTenancyTests(APITestCase):
    def setUp(self):
        self.org_a = Organization.objects.create(name="Org A")
        self.org_b = Organization.objects.create(name="Org B")
        self.admin_a = User.objects.create_user(
            username="admin_a", password="Str0ng-Pass-123",
            organization=self.org_a, role=User.Role.ADMIN,
        )
        self.member_a = User.objects.create_user(
            username="member_a", password="Str0ng-Pass-123",
            organization=self.org_a, role=User.Role.MEMBER,
        )
        self.admin_b = User.objects.create_user(
            username="admin_b", password="Str0ng-Pass-123",
            organization=self.org_b, role=User.Role.ADMIN,
        )
        self.doc = Document.objects.create(
            organization=self.org_a, title="Org A handbook", uploaded_by=self.admin_a
        )

    def upload(self, name="a.txt", content=b"hello world"):
        return {"title": "New", "file": SimpleUploadedFile(name, content)}

    def test_admin_can_create(self):
        self.client.force_authenticate(self.admin_a)
        res = self.client.post("/api/documents/", self.upload(), format="multipart")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Document.objects.get(id=res.data["id"]).organization, self.org_a)

    def test_member_can_list_but_not_create(self):
        self.client.force_authenticate(self.member_a)
        self.assertEqual(self.client.get("/api/documents/").status_code, 200)
        res = self.client.post("/api/documents/", self.upload(), format="multipart")
        self.assertEqual(res.status_code, 403)

    def test_other_org_cannot_see_documents(self):
        self.client.force_authenticate(self.admin_b)
        self.assertEqual(self.client.get("/api/documents/").data, [])
        self.assertEqual(self.client.get(f"/api/documents/{self.doc.id}/").status_code, 404)

    def test_other_org_cannot_delete(self):
        self.client.force_authenticate(self.admin_b)
        self.assertEqual(self.client.delete(f"/api/documents/{self.doc.id}/").status_code, 404)
        self.assertTrue(Document.objects.filter(id=self.doc.id).exists())

    def test_anonymous_is_rejected(self):
        self.assertEqual(self.client.get("/api/documents/").status_code, 401)

    def test_bad_extension_is_rejected(self):
        self.client.force_authenticate(self.admin_a)
        res = self.client.post("/api/documents/", self.upload("virus.exe"), format="multipart")
        self.assertEqual(res.status_code, 400)


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ProcessDocumentTests(APITestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="Org A")

    def make_doc(self, name, content):
        return Document.objects.create(
            organization=self.org, title="T", file=ContentFile(content, name=name)
        )

    def test_text_file_becomes_chunks(self):
        doc = self.make_doc("t.txt", ("word " * 500).encode())
        process_document(doc.id)
        doc.refresh_from_db()
        self.assertEqual(doc.status, Document.Status.READY)
        self.assertGreater(doc.chunks.count(), 1)
        self.assertEqual(doc.chunks.first().organization, self.org)

    def test_fake_pdf_is_marked_failed(self):
        doc = self.make_doc("bad.pdf", b"this is not a pdf")
        process_document(doc.id)
        doc.refresh_from_db()
        self.assertEqual(doc.status, Document.Status.FAILED)
        self.assertTrue(doc.error)

    def test_empty_file_is_marked_failed(self):
        doc = self.make_doc("empty.txt", b"   ")
        process_document(doc.id)
        doc.refresh_from_db()
        self.assertEqual(doc.status, Document.Status.FAILED)