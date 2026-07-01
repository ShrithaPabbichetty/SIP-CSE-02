
from simulationOutputMetrics import SimulationResult
from edgeDevice import EdgeDevice
from simulationInputMetrics import SimulationConfig
from Simulator import MultiEdgeSpeculativeSimulator
from plot import plot_results
import random

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
    plot_results(
        xpoints=[
            [0.5, 0.6, 0.7, 0.8, 0.9],
        ],
        y_list=[
            [283.54, 268.86, 232, 239.5, 202.8],
            [423.44, 358.398, 296.02, 289.798, 310.438],
            [470.44, 437.82, 330.76, 312.64, 294.92],
        ],
        xlabel="Draft Accuracy",
        ylabel="Latency",
        colors=["blue", "red", "green"],
        labels=["1 Device", "2 Devices", "3 Devices"],
        line_style=["-", "--", "-."],
        marker=["o", "s", "^"]
    )

    plot_results(
        xpoints=[1, 3, 5, 8, 10],
        y_list=[
            [260.56, 269.64, 267.84, 316.84, 342.44],
            [302.48, 290.34, 299.92, 333.98, 388.5],
            [360.54, 434.36, 392.84, 453.12, 430.2]
        ],
        xlabel="Communication Time",
        ylabel="Latency",
        colors=["blue", "red", "green"],
        labels=["Fast Devices", "Mixed Devices", "All Devices"],
        line_style=["-", "--", "-."],
        marker=["o", "s", "^"]
    )


if __name__ == "__main__":
    main()
