import unittest
import tempfile
import shutil
from pathlib import Path
from framework.standards import FileStorageManager

class TestFileStorageManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.storage = FileStorageManager(upload_dir=self.temp_dir, max_file_size_bytes=1000)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_sanitize_filename(self):
        filename = "../../etc/passwd/minha_imagem!!@#.png"
        clean = FileStorageManager.sanitize_filename(filename)
        self.assertEqual(clean, "minha_imagem_.png")
        self.assertNotIn("..", clean)

    def test_allowed_extension(self):
        self.assertTrue(self.storage.is_allowed_extension("document.pdf"))
        self.assertFalse(self.storage.is_allowed_extension("script.exe"))

    def test_save_file_success(self):
        content = b"Conteudo de teste"
        success, filepath = self.storage.save_file("relatorio.pdf", content)
        self.assertTrue(success)
        self.assertTrue(Path(filepath).exists())

    def test_save_file_exceed_size(self):
        large_content = b"X" * 2000
        success, error = self.storage.save_file("documento.txt", large_content)
        self.assertFalse(success)
        self.assertIn("excede o limite", error)

if __name__ == "__main__":
    unittest.main()
