from dataclasses import dataclass

@dataclass
class SimulationResult:
    accuracy: float
    latency: float
    numOfAcceptedTokens: int
    numOfRejectedTokens: int
    num_devices: int
    is_async: bool
    draft_calls: int 
    verifier_calls: int
