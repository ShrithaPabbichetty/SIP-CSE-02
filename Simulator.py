from simulationOutputMetrics import SimulationResult
from edgeDevice import EdgeDevice
import random


def run_baseline(response_length, verifier_token_time):
    return SimulationResult(
        latency=verifier_token_time * response_length,
        accuracy=None,
        numOfAcceptedTokens=0,
        numOfRejectedTokens=0,
        num_devices=1,
        is_async=False
    )


def simulate_round(device, tokens_remaining, speculative_window, rnd):
    accepted = 0
    rejected = 0
    
    draft_size = min(
        device.numberOftokensGenerated, 
        tokens_remaining,
        speculative_window
    )
    
    for i in range(draft_size):
        if rnd.random() < device.accuracyprediction:
            accepted += 1
        else:
            rejected += 1
            break

    return accepted, rejected


def run_multi_edge_sync(devices, response_length, verifier_token_time, speculative_window, seed=10):
    rnd = random.Random(seed)

    total_accepted, total_rejected, total_generated = 0, 0, 0
    draft_calls, verifier_calls = 0, 0
    rounds = 0
    total_latency = 0.0

    round_schedule = [
        [devices[0], devices[2]],
        [devices[1], devices[2], devices[3]],
        [devices[0], devices[3]],
    ]

    while total_generated < response_length:
        schedule = round_schedule[rounds % len(round_schedule)]
        rounds += 1

        tokens_remaining = response_length - total_generated
        candidates = []
        arrival_times = []

        for device in schedule:
            accepted, rejected = simulate_round(device, tokens_remaining, speculative_window, rnd)
            tokens_attempted = accepted + rejected

            arrival_time = device.communication_time + (device.draft_token_time * tokens_attempted)
            arrival_times.append(arrival_time)
            candidates.append({
                "device": device,
                "accepted": accepted,
                "rejected": rejected,
                "arrival_time": arrival_time
            })
            draft_calls += 1

        # Verifier waits for ALL devices to finish before it can start checking
        barrier = max(arrival_times)
        verifier_calls += 1

        # Pick the best candidate (the one with the earliest arrival time)
        candidates.sort(key=lambda x: x["arrival_time"])
        best = candidates[0]

        round_latency = barrier + verifier_token_time

        if best["rejected"] > 0:
            tokens_advanced = min(best["accepted"] + 1, tokens_remaining)
        else:
            tokens_advanced = min(best["accepted"], tokens_remaining)

        total_accepted += best["accepted"]
        total_rejected += best["rejected"]
        total_generated += tokens_advanced
        total_latency += round_latency

        print("Round", rounds,
              "| selected device:", [d.device_id for d in schedule],
              "| device:", best["device"].device_id,
              "| accepted:", best["accepted"],
              "| rejected:", best["rejected"],
              "| advanced:", tokens_advanced,
              "| total:", total_generated, "/", response_length,
              "| barrier:", round(barrier, 2),
              "| roundLatency:", round(round_latency, 2))

    if total_accepted + total_rejected > 0: 
        total_accuracy = total_accepted / (total_accepted + total_rejected)
    else:
        total_accuracy = 0.0

    return SimulationResult(
        latency=total_latency,
        accuracy=total_accuracy,
        numOfAcceptedTokens=total_accepted,
        numOfRejectedTokens=total_rejected,
        num_devices=len(devices),
        is_async=False
    )


def main():
    device1 = EdgeDevice(device_id="device-1", draft_token_time=5.6, accuracyprediction=0.9, numberOftokensGenerated=10, communication_time=6.7)
    device2 = EdgeDevice(device_id="device-2", draft_token_time=9.2, accuracyprediction=0.6, numberOftokensGenerated=4, communication_time=3.3)
    device3 = EdgeDevice(device_id="device-3", draft_token_time=6.2, accuracyprediction=0.7, numberOftokensGenerated=3, communication_time=3.1)
    device4 = EdgeDevice(device_id="device-4", draft_token_time=7.1, accuracyprediction=0.75, numberOftokensGenerated=3, communication_time=2.8)

    response_length = 10
    verifier_time = 30
    target_token_time = 40
    speculative_window = 3
    seed = 10
    

    baseline = run_baseline(response_length, target_token_time)
    print("Baseline latency:", baseline.latency)

    print("\nSimulating multi-device response:")
    multi_result = run_multi_edge_sync([device1, device2, device3, device4], response_length, verifier_time, speculative_window, seed)
    print(multi_result)

    speedup = baseline.latency / multi_result.latency
    print("\nSpeedup of multi-device over baseline:", round(speedup, 2))


if __name__ == "__main__":
    main()
