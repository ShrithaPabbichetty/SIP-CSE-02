from simulationOutputMetrics import SimulationResult
from edgeDevice import EdgeDevice
import random


class MultiEdgeSpeculativeSimulator:
    def __init__(self, devices, response_length, verifier_token_time, speculative_window, seed=10):
        self.devices = devices
        self.response_length = response_length
        self.verifier_token_time = verifier_token_time
        self.speculative_window = speculative_window
        self.rnd = random.Random(seed)

        self.round_schedule = [
            [devices[0], devices[2]],
            [devices[1], devices[2], devices[3]],
            [devices[0], devices[3]],
        ]

    def run_baseline(self, response_length, verifier_token_time):
        return SimulationResult(
            latency=verifier_token_time * response_length,
            accuracy=None,
            numOfAcceptedTokens=0,
            numOfRejectedTokens=0,
            num_devices=1,
            is_async=False
        )

    def simulate_round(self, device, tokens_remaining):
        accepted = 0
        rejected = 0

        draft_size = min(
            device.numberOftokensGenerated,
            tokens_remaining,
            self.speculative_window
        )

        for i in range(draft_size):
            if self.rnd.random() < device.accuracyprediction:
                accepted += 1
            else:
                rejected += 1
                break

        return accepted, rejected

    def get_round_schedule(self, rounds):
        return self.round_schedule[rounds % len(self.round_schedule)]

    def simulate_device_draft(self, device, tokens_remaining):
        accepted, rejected = self.simulate_round(device, tokens_remaining)
        tokens_attempted = accepted + rejected
        arrival_time = device.communication_time + (device.draft_token_time * tokens_attempted)

        return {
            "device": device,
            "accepted": accepted,
            "rejected": rejected,
            "arrival_time": arrival_time
        }

    def select_winning_candidate(self, candidates):
        return min(candidates, key=lambda x: x["arrival_time"])

    def compute_round_latency(self, arrival_times):
        barrier = max(arrival_times)
        round_latency = barrier + self.verifier_token_time
        return barrier, round_latency

    def run(self):
        total_accepted, total_rejected, total_generated = 0, 0, 0
        draft_calls, verifier_calls = 0, 0
        rounds = 0
        total_latency = 0.0

        while total_generated < self.response_length:
            schedule = self.get_round_schedule(rounds)
            rounds += 1

            tokens_remaining = self.response_length - total_generated

            candidates = []
            for device in schedule:
                candidate = self.simulate_device_draft(device, tokens_remaining)
                candidates.append(candidate)
                draft_calls += 1

            arrival_times = [c["arrival_time"] for c in candidates]

            # Verifier waits for ALL devices to finish before it can start checking
            verifier_calls += 1

            best = self.select_winning_candidate(candidates)
            barrier, round_latency = self.compute_round_latency(arrival_times)

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
                  "| total:", total_generated, "/", self.response_length,
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
            num_devices=len(self.devices),
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

    sim = MultiEdgeSpeculativeSimulator(
        [device1, device2, device3, device4],
        response_length,
        verifier_time,
        speculative_window,
        seed
    )

    baseline = sim.run_baseline(response_length, target_token_time)
    print("Baseline latency:", baseline.latency)

    print("\nSimulating multi-device response:")
    multi_result = sim.run()
    print(multi_result)

    speedup = baseline.latency / multi_result.latency
    print("\nSpeedup of multi-device over baseline:", round(speedup, 2))


if __name__ == "__main__":
    main()
