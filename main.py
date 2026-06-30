
from simulationOutputMetrics import SimulationResult
from edgeDevice import EdgeDevice
from simulationInputMetrics import SimulationConfig
from Simulator import MultiEdgeSpeculativeSimulator
from plot import plot_results
import random
import matplotlib.pyplot as plt
import numpy as np

def main():
    device1 = EdgeDevice(device_id="device-1", draft_token_time=5.6, accuracyprediction=0.9, numberOftokensGenerated=10, communication_time=6.7)
    device2 = EdgeDevice(device_id="device-2", draft_token_time=9.2, accuracyprediction=0.6, numberOftokensGenerated=4, communication_time=3.3)
    device3 = EdgeDevice(device_id="device-3", draft_token_time=6.2, accuracyprediction=0.7, numberOftokensGenerated=3, communication_time=3.1)
    device4 = EdgeDevice(device_id="device-4", draft_token_time=7.1, accuracyprediction=0.75, numberOftokensGenerated=3, communication_time=2.8)

    devices = [device1, device2, device3, device4]

    config = SimulationConfig(
        num_devices=len(devices),
        is_async=False,
        device_ids=devices,
        response_length=10,
        target_token_time=40,
        verifier_time=30,
        speculative_window=3,
        seed=10,
        round_schedule=[
            [device1, device3],
            [device2, device3, device4],
            [device1, device4],
        ]
    )

    sim = MultiEdgeSpeculativeSimulator(config)

    baseline = sim.run_baseline()
    print("Baseline latency:", baseline.latency)

    print("\nSimulating multi-device response:")
    multi_result = sim.run()
    print(multi_result)

    speedup = baseline.latency / multi_result.latency
    print("\nSpeedup of multi-device over baseline:", round(speedup, 2))
    
    # Plot the results
    plot_results(xpoints=[0.5, 0.6, 0.7, 0.8, 0.9], ypoints=[427.1, 406.2, 316.9, 316.9, 222], xlabel="Draft Accuracy", ylabel="Latency")
    plot_results(xpoints=[1, 3, 5, 8, 10], ypoints=[320.7, 334.7, 348.7, 369.7, 383.7], xlabel="Communication Time", ylabel="Latency")


if __name__ == "__main__":
    main()
