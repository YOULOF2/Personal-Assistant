from loguru import logger
from source.backend import PersonalAssistant

logger.add("file.log", rotation="1 week")

PersonalAssistant().process("What is your favourite food")
