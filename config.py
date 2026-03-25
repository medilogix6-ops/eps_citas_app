import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Nombre del hospital donde atienden todos los médicos del sistema."""
    MEDICO_HOSPITAL_DEFAULT = os.environ.get(
        'MEDICO_HOSPITAL', 'IPS Clinica Meira Del Mar'
    )

    SECRET_KEY      = os.environ.get('SECRET_KEY', 'eps-citas-secret-2025')
    MYSQL_HOST      = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT      = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER      = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD  = os.environ.get('MYSQL_PASSWORD', '12345')
    MYSQL_DB        = os.environ.get('MYSQL_DATABASE', 'railway')
