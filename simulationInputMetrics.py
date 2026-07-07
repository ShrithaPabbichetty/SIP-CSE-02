from dataclasses import dataclass, field


@dataclass
class SimulationConfig:
    num_devices: int
    is_async: bool
    device_ids: list[str]
    response_length: int
    target_token_time: float
    verifier_time: float
    speculative_window: int
    seed: int = 10
    round_schedule: list[list[str]] = field(default_factory=list)
    scheduling_policy: str = "manual"
