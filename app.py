#!/usr/bin/env python3

import logging

logging.basicConfig(filename="myapp.log", level=logging.INFO, filemode='w',
                    format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
handler = logging.FileHandler("test.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s -%(name)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Testing custom logger")
