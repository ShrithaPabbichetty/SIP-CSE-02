from dataclasses import dataclass
@dataclass
class EdgeDevice:
    device_id: str
    draft_token_time: float
    accuracy: float
    number_of_tokens_generated: int
    communication_time: float
