import re
import logging
import os
from dataclasses import dataclass


@dataclass
class CartUpdateModel:
    item_id: str
    session_id: str