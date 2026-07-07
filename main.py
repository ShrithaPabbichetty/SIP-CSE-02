from simulationOutputMetrics import SimulationResult
from edgeDevice import EdgeDevice
from simulationInputMetrics import SimulationConfig
from Simulator import MultiEdgeSpeculativeSimulator
import random

def select_fastest_devices(devices, top_n=2):
    def calculate_total_latency(device):
        return (device.draft_token_time * device.number_of_tokens_generated) + device.communication_time
    
    sorted_devices = sorted(devices, key=calculate_total_latency)
    return sorted_devices[:top_n]

def main():
    device1 = EdgeDevice(device_id="device-1", draft_token_time=5.6, accuracy=0.9, number_of_tokens_generated=10, communication_time=10)
    device2 = EdgeDevice(device_id="device-2", draft_token_time=9.2, accuracy=0.6, number_of_tokens_generated=4, communication_time=10)
    device3 = EdgeDevice(device_id="device-3", draft_token_time=6.2, accuracy=0.7, number_of_tokens_generated=3, communication_time=10)
    device4 = EdgeDevice(device_id="device-4", draft_token_time=7.1, accuracy=0.75, number_of_tokens_generated=3, communication_time=10)

    devices = [device1,device2,device3,device4]
    
    selected_devices = select_fastest_devices(devices, top_n=2)
    
    print(f"Selected Devices: {[d.device_id for d in selected_devices]}")

    config = SimulationConfig(
        num_devices=len(selected_devices),
        is_async=False,
        device_ids=selected_devices,
        response_length=10,
        target_token_time=40,
        verifier_time=30,
        speculative_window=3,
        seed=random.random(),
        round_schedule=[selected_devices] 
    )

    sim = MultiEdgeSpeculativeSimulator(config)

    baseline = sim.run_baseline()
    print("Baseline latency:", baseline.latency)

    print("\nSimulating multi-device response:")
    multi_result = sim.run()
    print(multi_result)

    speedup = baseline.latency / multi_result.latency
    print("\nSpeedup of multi-device over baseline:", round(speedup, 1))

if __name__ == "__main__":
    main()