from simulationOutputMetrics import SimulationResult
from edgeDevice import EdgeDevice
from simulationInputMetrics import SimulationConfig
import random


class MultiEdgeSpeculativeSimulator:
    def __init__(self, simulation_config):
        self.config = simulation_config

        self.devices = simulation_config.device_ids
        self.num_devices = simulation_config.num_devices
        self.is_async = simulation_config.is_async
        self.response_length = simulation_config.response_length
        self.target_token_time = simulation_config.target_token_time
        self.verifier_token_time = simulation_config.verifier_time
        self.speculative_window = simulation_config.speculative_window
        self.seed = simulation_config.seed
        self.rnd = random.Random(self.seed)

        self.round_schedule = simulation_config.round_schedule or [
            [self.devices[0], self.devices[2]],
            [self.devices[1], self.devices[2], self.devices[3]],
            [self.devices[0], self.devices[3]],
        ]

    def run_baseline(self):
        return SimulationResult(
            latency=self.target_token_time * self.response_length,
            accuracy=None,
            num_of_accepted_tokens=0,
            num_of_rejected_tokens=0,
            num_devices=1,
            is_async=False,
            draft_calls=0,
            verifier_calls=0
        )

    def simulate_round(self, device, tokens_remaining):
        accepted = 0
        rejected = 0

        draft_size = min(
            device.number_of_tokens_generated,
            tokens_remaining,
            self.speculative_window
        )

        for i in range(draft_size):
            if self.rnd.random() < device.accuracy:
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
        if self.is_async:
            barrier = min(arrival_times)
        else:
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
            num_of_accepted_tokens=total_accepted,
            num_of_rejected_tokens=total_rejected,
            num_devices=self.num_devices,
            is_async=self.is_async,
            draft_calls=draft_calls,
            verifier_calls=verifier_calls
        )
