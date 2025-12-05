import sys
from loguru import logger

logger.remove()

logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <green>{level}</green> | <light-blue>{message}</light-blue>",
    level="INFO",
)
