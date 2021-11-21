import logging
import click
import pandas
from pathlib import Path

logging.basicConfig(
    level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)

logger = logging.getLogger(__name__)


def converter():
    logger.info("teste")
    print("hello world")
