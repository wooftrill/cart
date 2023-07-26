import re
import logging
import os
from dataclasses import dataclass


@dataclass
class CheckoutModel:
    session_id: str
    checkout_details: str

