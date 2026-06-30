from dataclasses import dataclass

@dataclass
class SimulationConfig:
    num_devices: int
    is_async: bool
    device_ids: list[str]
    max_response_length: int