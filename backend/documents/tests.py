from rest_framework.test import APITestCase

from accounts.models import Organization, User
from .models import Document


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

    def test_admin_can_create(self):
        self.client.force_authenticate(self.admin_a)
        res = self.client.post("/api/documents/", {"title": "New"})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Document.objects.get(id=res.data["id"]).organization, self.org_a)

    def test_member_can_list_but_not_create(self):
        self.client.force_authenticate(self.member_a)
        self.assertEqual(self.client.get("/api/documents/").status_code, 200)
        self.assertEqual(self.client.post("/api/documents/", {"title": "X"}).status_code, 403)

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