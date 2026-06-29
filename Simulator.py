from simulationOutputMetrics import SimulationResult
from edgeDevice import EdgeDevice
import random


def baselineMetrics(response_length, token_time):
    return SimulationResult(
        latency=token_time * response_length,
        accuracy=None,
        numOfAcceptedTokens=response_length,
        numOfRejectedTokens=0,
        num_devices=1,
        is_async=False,
        verifierCalls=0,
        draftCalls=0,
        speedup_vs_baseline=None,
    )


def simulateRound(device, tokensRemaining, speculative_window, rnd):
    accepted = 0
    rejected = 0
    max_tokens = min(tokensRemaining, speculative_window)
    for _ in range(max_tokens):
        if rnd.random() < device.accuracypredcttion:
            accepted += 1
        else:
            rejected += 1
            break
    return accepted, rejected


def simulateResponse(device, response_length, speculative_window=1, verifier_step_time=0.0, seed=None):
    rnd = random.Random(seed)
    totalaccepted = 0
    totalrejected = 0
    totalGenerated = 0
    latency = 0.0
    verifier_calls = 0
    draft_calls = 0

    while totalGenerated < response_length:
        accepted, rejected = simulateRound(device, response_length - totalGenerated, speculative_window, rnd)
        totalaccepted += accepted
        totalrejected += rejected
        totalGenerated += accepted + rejected
        verifier_calls += 1
        draft_calls += 1
        latency += verifier_step_time
        latency += device.draft_token_time * (accepted + rejected)

    baseline_latency = baselineMetrics(response_length, device.draft_token_time).latency
    speedup = baseline_latency / latency if latency > 0 else None

    return SimulationResult(
        latency=latency,
        accuracy=device.accuracypredcttion,
        numOfAcceptedTokens=totalaccepted,
        numOfRejectedTokens=totalrejected,
        num_devices=1,
        is_async=False,
        verifierCalls=verifier_calls,
        draftCalls=draft_calls,
        speedup_vs_baseline=speedup,
    )


def simulateMultiDevice(devices, response_length, speculative_window=1, verifier_step_time=0.0, seed=None):
    rnd = random.Random(seed)
    totalAccepted = 0
    totalRejected = 0
    totalGenerated = 0
    latency = 0.0
    verifier_calls = 0
    draft_calls = 0

    # parallel rounds
    while totalGenerated < response_length:
        round_results = []  # (accepted, rejected, device)
        for d in devices:
            if totalGenerated >= response_length:
                break
            accepted, rejected = simulateRound(d, response_length - totalGenerated, speculative_window, rnd)
            round_results.append((accepted, rejected, d))
            totalAccepted += accepted
            totalRejected += rejected
            totalGenerated += accepted + rejected
            draft_calls += 1

        verifier_calls += 1

        max_arrival = 0.0
        for accepted_tokens, rejected_tokens, device in round_results:
            draft_size = accepted_tokens + rejected_tokens
            arrival_time = device.draft_token_time * draft_size + device.comm_delay
            if arrival_time > max_arrival:
                max_arrival = arrival_time
        roundLatency = max_arrival + verifier_step_time
        latency += roundLatency

    device1_token_time = devices[0].draft_token_time
    baseline_latency = baselineMetrics(response_length, device1_token_time).latency
    speedup = baseline_latency / latency if latency > 0 else None

    return SimulationResult(
        latency=latency,
        accuracy=None,
        numOfAcceptedTokens=totalAccepted,
        numOfRejectedTokens=totalRejected,
        num_devices=len(devices),
        is_async=False,
        verifierCalls=verifier_calls,
        draftCalls=draft_calls,
        speedup_vs_baseline=speedup,
    )


def main():
    devices = [
        EdgeDevice(device_id="device_1", draft_token_time=0.9, accuracypredcttion=0.2, numberOftokensGenerated=10, comm_delay=0.1),
        EdgeDevice(device_id="device_2", draft_token_time=0.1, accuracypredcttion=0.5, numberOftokensGenerated=12, comm_delay=0.25),
        EdgeDevice(device_id="device_3", draft_token_time=0.3, accuracypredcttion=0.1, numberOftokensGenerated=8, comm_delay=0.2),
    ]
    response_length = 10
    speculative_window = 3
    verifier_step_time = 0.05
    seed = 10

    result_single = simulateResponse(devices[0], response_length, speculative_window=speculative_window, verifier_step_time=verifier_step_time, seed=seed)
    print("Single-device result:", result_single)

    result_multi = simulateMultiDevice(devices, response_length, speculative_window=speculative_window, verifier_step_time=verifier_step_time, seed=seed)
    print("Multi-device result:", result_multi)


if __name__ == "__main__":
    main()
