import json
import unittest

from framework.standards import OpenAPIGenerator


class TestOpenAPIGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = OpenAPIGenerator(title="Test API", version="2.0.0", description="API de Teste")

    def test_add_path_and_to_json(self):
        self.generator.add_path(
            path="/users",
            method="POST",
            summary="Cria um novo usuário",
            responses={"201": {"description": "Usuário criado com sucesso"}},
            request_body={"content": {"application/json": {"schema": {"type": "object"}}}},
            tags=["Usuários"]
        )

        spec_dict = self.generator.to_dict()
        self.assertIn("/users", spec_dict["paths"])
        self.assertIn("post", spec_dict["paths"]["/users"])
        self.assertEqual(spec_dict["info"]["title"], "Test API")

        spec_json = self.generator.to_json()
        parsed = json.loads(spec_json)
        self.assertEqual(parsed["openapi"], "3.0.3")

if __name__ == "__main__":
    unittest.main()
