
from simulationOutputMetrics import SimulationResult
from edgeDevice import EdgeDevice
from simulationInputMetrics import SimulationConfig
from Simulator import MultiEdgeSpeculativeSimulator
from plot import plot_results
import random

def main():
    device1 = EdgeDevice(device_id="device-1", draft_token_time=5.6, accuracy=0.9, number_of_tokens_generated=10, communication_time=6.7)
    device2 = EdgeDevice(device_id="device-2", draft_token_time=9.2, accuracy=0.6, number_of_tokens_generated=4, communication_time=3.3)
    device3 = EdgeDevice(device_id="device-3", draft_token_time=6.2, accuracy=0.7, number_of_tokens_generated=3, communication_time=3.1)
    device4 = EdgeDevice(device_id="device-4", draft_token_time=7.1, accuracy=0.75, number_of_tokens_generated=3, communication_time=2.8)

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

    # ---- Draft Accuracy latency data (avg / min / max) ----
    avg_1 = [283.54, 268.86, 232.0, 239.5, 202.8]
    min_1 = [239.5, 202.8, 202.0, 202.8, 202.8]
    max_1 = [312.9, 349.6, 312.9, 276.2, 202.8]

    avg_2 = [423.44, 358.398, 296.02, 289.798, 310.438]
    min_2 = [282.3, 278.7, 227.0, 225.2, 225.2]
    max_2 = [524.2, 422.79, 332.2, 352.7, 439.19]

    avg_3 = [470.44, 437.82, 330.76, 312.64, 294.92]
    min_3 = [411.6, 372.9, 227.0, 271.3, 271.3]
    max_3 = [519.8, 542.6, 391.3, 393.1, 323.0]

    yerr_list_accuracy = [
        [[a - lo for a, lo in zip(avg_1, min_1)], [hi - a for a, hi in zip(avg_1, max_1)]],
        [[a - lo for a, lo in zip(avg_2, min_2)], [hi - a for a, hi in zip(avg_2, max_2)]],
        [[a - lo for a, lo in zip(avg_3, min_3)], [hi - a for a, hi in zip(avg_3, max_3)]],
    ]

    plot_results(
        xpoints=[
            [0.5, 0.6, 0.7, 0.8, 0.9],
        ],
        y_list=[
            avg_1,
            avg_2,
            avg_3,
        ],
        xlabel="Draft Accuracy",
        ylabel="Latency",
        colors=["blue", "red", "green"],
        labels=["1 Device", "2 Devices", "3 Devices"],
        line_style=["-", "--", "-."],
        marker=["o", "s", "^"],
        yerr_list=yerr_list_accuracy
    )

    # ---- Communication Time latency data (avg / min / max) ----
    avg_fast = [260.56, 269.64, 267.84, 316.84, 342.44]
    min_fast = [221.4, 231.4, 241.4, 256.4, 232.6]
    max_fast = [325.8, 330.4, 304.4, 416.6, 444.4]

    avg_mixed = [302.48, 290.34, 299.92, 333.98, 388.5]
    min_mixed = [247.3, 212.7, 215.4, 227.4, 292.2]
    max_mixed = [337.6, 351.6, 365.6, 391.0, 507.1]

    avg_all = [360.54, 434.36, 392.84, 453.12, 430.2]
    min_all = [277.5, 366.2, 322.0, 380.9, 312.8]
    max_all = [406.4, 485.5, 482.8, 535.9, 477.4]

    yerr_list_comm = [
        [[a - lo for a, lo in zip(avg_fast, min_fast)], [hi - a for a, hi in zip(avg_fast, max_fast)]],
        [[a - lo for a, lo in zip(avg_mixed, min_mixed)], [hi - a for a, hi in zip(avg_mixed, max_mixed)]],
        [[a - lo for a, lo in zip(avg_all, min_all)], [hi - a for a, hi in zip(avg_all, max_all)]],
    ]

    plot_results(
        xpoints=[1, 3, 5, 8, 10],
        y_list=[
            avg_fast,
            avg_mixed,
            avg_all,
        ],
        xlabel="Communication Time",
        ylabel="Latency",
        colors=["blue", "red", "green"],
        labels=["Fast Devices", "Mixed Devices", "All Devices"],
        line_style=["-", "--", "-."],
        marker=["o", "s", "^"],
        yerr_list=yerr_list_comm
    )


if __name__ == "__main__":
    main()
    main()
