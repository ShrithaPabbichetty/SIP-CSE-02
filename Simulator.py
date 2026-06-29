from simulationOutputMetrics import SimulationResult
from edgeDevice import EdgeDevice
import random


def baselineMetrics(response_length, token_time, verifier_time):
    return SimulationResult(
        latency=(token_time + verifier_time) * response_length,
        accuracy=None,
        numOfAcceptedTokens=response_length,
        numOfRejectedTokens=0,
        num_devices=1,
        is_async=False
    )


def simulateRound(device, tokensRemaining):
    accepted = 0
    rejected = 0
    draft_size = min(device.numberOftokensGenerated, tokensRemaining)
    for i in range(draft_size):
        if random.random() < device.accuracyprediction:
            accepted += 1
        else:
            rejected += 1
            break
    return accepted, rejected


def simulateMulti(devices, response_length, verifier_time):
    totalaccepted, totalrejected, totalGenerated = 0, 0, 0
    totalLatency = 0.0
    roundNum = 0

    roundSchedule = [
        [devices[0], devices[2]],
        [devices[1], devices[2], devices[3]],
        [devices[0], devices[3]],
    ]

    while totalGenerated < response_length:
        schedule = roundSchedule[roundNum % len(roundSchedule)]
        roundNum += 1

        tokensRemaining = response_length - totalGenerated
        candidates = []
        arrival_times = []

        for device in schedule:
            accepted, rejected = simulateRound(device, tokensRemaining)
            tokensAttempted = accepted + rejected
            arrival_time = device.communication_time + (device.draft_token_time * tokensAttempted)
            arrival_times.append(arrival_time)
            candidates.append({
                "device": device,
                "accepted": accepted,
                "rejected": rejected,
                "arrival_time": arrival_time
            })

        # Verifier waits for ALL devices to finish before it can start checking
        barrier = max(arrival_times)

        # Pick the best candidate (most accepted tokens)
        candidates.sort(key=lambda x: x["arrival_time"])
        best = candidates[0]

        round_latency = barrier + verifier_time

        if best["rejected"] > 0:
            tokensAdvanced = min(best["accepted"] + 1, tokensRemaining)
        else:
            tokensAdvanced = min(best["accepted"], tokensRemaining)

        totalaccepted += best["accepted"]
        totalrejected += best["rejected"]
        totalGenerated += tokensAdvanced
        totalLatency += round_latency

        print("Round", roundNum,
              "| device:", best["device"].device_id,
              "| accepted:", best["accepted"],
              "| rejected:", best["rejected"],
              "| advanced:", tokensAdvanced,
              "| total:", totalGenerated, "/", response_length,
              "| barrier:", round(barrier, 2),
              "| roundLatency:", round(round_latency, 2))

    totalAccuracy = 0
    for d in devices:
        totalAccuracy += d.accuracyprediction
    averageAccuracy = totalAccuracy / len(devices)

    return SimulationResult(
        latency=totalLatency,
        accuracy=averageAccuracy,
        numOfAcceptedTokens=totalaccepted,
        numOfRejectedTokens=totalrejected,
        num_devices=len(devices),
        is_async=False
    )


def main():
    device1 = EdgeDevice(device_id="device-1", draft_token_time=0.5, accuracyprediction=0.9, numberOftokensGenerated=10, communication_time=0.1)
    device2 = EdgeDevice(device_id="device-2", draft_token_time=0.15, accuracyprediction=0.6, numberOftokensGenerated=4, communication_time=0.2)
    device3 = EdgeDevice(device_id="device-3", draft_token_time=0.2, accuracyprediction=0.7, numberOftokensGenerated=3, communication_time=0.3)
    device4 = EdgeDevice(device_id="device-4", draft_token_time=0.3, accuracyprediction=0.75, numberOftokensGenerated=3, communication_time=0.4)

    response_length = 10
    verifier_time = 0.5

    baseline = baselineMetrics(response_length, device1.draft_token_time, verifier_time)
    print("Baseline latency:", baseline.latency)

    print("\nSimulating multi-device response:")
    multi_result = simulateMulti([device1, device2, device3, device4], response_length, verifier_time)
    print(multi_result)

    speedup = baseline.latency / multi_result.latency
    print("\nSpeedup of multi-device over baseline:", round(speedup, 2))


if __name__ == "__main__":
    main()
