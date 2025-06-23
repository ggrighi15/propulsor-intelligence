from __future__ import annotations
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(os.getenv("PROPULSOR_ROOT", Path(__file__).resolve().parent))
DATA_DIR = ROOT_DIR / "data"
EMAIL_DIR = ROOT_DIR / "emails"
DATA_DIR.mkdir(parents=True, exist_ok=True)
EMAIL_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
