from dataclasses import dataclass

@dataclass
class SimulationConfig:
    num_devices: int
    is_async: bool
    device_ids: list[str]
    maxResponseLength: int