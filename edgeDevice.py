from dataclasses import dataclass
@dataclass
class EdgeDevice:
    device_id: str
    draft_token_time: float
    accuracyprediction: float
    numberOftokensGenerated: int
    communication_time: float
