from dataclasses import dataclass

@dataclass
class Error:
    message: str
    message_id: str
    type: str