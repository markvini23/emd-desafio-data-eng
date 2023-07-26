"""
Constants for all flows
"""
from enum import Enum


class Constants(Enum):
    """
    Constants used in the project
    """

    OUTPUT_DIR = "db/output"
    DB_ENGINE = "postgresql://postgres:postgres_password@localhost:5432/brt-gps"
    API_URL = "https://dados.mobilidade.rio/gps/brt"
