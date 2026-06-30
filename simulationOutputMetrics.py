from dataclasses import dataclass

@dataclass
class SimulationResult:
    accuracy: float
    latency: float
    num_of_acceptedTokens: int
    num_of_rejectedTokens: int
    num_devices: int
    is_async: bool
