from .__main__ import init_db
from .logger import logger
from software.sailowtech_ctd.webapi.app import app, start

init_db()