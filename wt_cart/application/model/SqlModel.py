import re
import logging
import os
from dataclasses import dataclass


@dataclass
class SqlModel:
    session_id: str
    cart_id: str
    item_id: str
    count: int
    is_active: int