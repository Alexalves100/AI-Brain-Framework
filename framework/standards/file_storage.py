"""
File Storage Manager Module.
Gerencia upload, armazenamento e sanitização de arquivos de forma segura,
prevenindo vulnerabilidades como Path Traversal, Execução Indesejada e DoS por arquivos grandes.
"""
import os
import re
from pathlib import Path
from typing import Optional, Set, Tuple


class FileStorageManager:
    """Gerenciador seguro de arquivos e uploads."""

    DEFAULT_ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".json", ".csv", ".txt", ".svg"}
    DEFAULT_MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

    def __init__(
        self,
        upload_dir: str = "uploads",
        allowed_extensions: Optional[Set[str]] = None,
        max_file_size_bytes: int = DEFAULT_MAX_SIZE_BYTES,
    ):
        self.upload_dir = Path(upload_dir)
        self.allowed_extensions = allowed_extensions or self.DEFAULT_ALLOWED_EXTENSIONS
        self.max_file_size = max_file_size_bytes
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        if not self.upload_dir.exists():
            self.upload_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """Sanitiza o nome do arquivo prevenindo Path Traversal e caracteres perigosos."""
        # Pega apenas o nome base
        name = os.path.basename(filename)
        # Remove caracteres que não sejam alfanuméricos, hífen, underline ou ponto
        clean_name = re.sub(r"[^\w\.-]", "_", name)
        clean_name = re.sub(r"_{2,}", "_", clean_name)
        clean_name = re.sub(r"\.{2,}", ".", clean_name)
        return clean_name.strip("._") or "file_upload"


    def is_allowed_extension(self, filename: str) -> bool:
        """Verifica se a extensão do arquivo está na whitelist de extensões permitidas."""
        ext = Path(filename).suffix.lower()
        return ext in self.allowed_extensions

    def validate_file(self, filename: str, file_size: int) -> Tuple[bool, Optional[str]]:
        """Valida extensão e tamanho do arquivo."""
        if not self.is_allowed_extension(filename):
            ext = Path(filename).suffix.lower()
            return False, f"Extensão de arquivo '{ext}' não é permitida."

        if file_size > self.max_file_size:
            max_mb = self.max_file_size / (1024 * 1024)
            return False, f"Arquivo excede o limite máximo permitido de {max_mb:.1f} MB."

        return True, None

    def save_file(self, filename: str, content: bytes) -> Tuple[bool, str]:
        """Sanitiza, valida e salva o conteúdo do arquivo no diretório de upload."""
        safe_name = self.sanitize_filename(filename)
        is_valid, error = self.validate_file(safe_name, len(content))
        if not is_valid:
            return False, error or "Erro de validação"

        destination = self.upload_dir / safe_name
        try:
            with open(destination, "wb") as f:
                f.write(content)
            return True, str(destination.resolve())
        except Exception as e:
            return False, f"Falha ao salvar arquivo: {str(e)}"
