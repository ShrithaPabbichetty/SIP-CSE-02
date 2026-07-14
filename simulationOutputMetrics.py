from dataclasses import dataclass

@dataclass
class SimulationResult:
    accuracy: float
    latency: float
    num_of_accepted_tokens: int
    num_of_rejected_tokens: int
    num_devices: int
    is_async: bool
    draft_calls: int 
    verifier_calls: int
