import random
from edgeDevice import EdgeDevice
from simulationInputMetrics import SimulationConfig
from simulationOutputMetrics import SimulationResult

class Simulator:
    def __init__(self, config: SimulationConfig, devices: list[EdgeDevice], 
                 speculative_window: int, verifier_step_time: float):
        self.config = config
        self.devices = devices
        self.speculative_window = speculative_window
        self.verifier_step_time = verifier_step_time

        
        self.total_latency = 0.0
        self.accepted_tokens = 0
        self.rejected_tokens = 0

    def run(self) -> SimulationResult:
        total_generated = 0
        round_number = 0
        print(f"\n--- Simulation Starting (Total tokens: {self.config.maxResponseLength}) ---")
        
        while total_generated < self.config.maxResponseLength:
            actual_round = round_number % 4
            
            # Selección de dispositivos según la ronda
            if actual_round == 0:
                dispositivos_activos = [self.devices[0], self.devices[2]]
            elif actual_round == 1:
                dispositivos_activos = [self.devices[1]]
            elif actual_round == 2:
                dispositivos_activos = [self.devices[0], self.devices[1], self.devices[2]]
            else:
                dispositivos_activos = [self.devices[0], self.devices[1], self.devices[2]]

            device = random.choice(dispositivos_activos)
            
            print(f"Round {round_number} | Using: {device.device_id}")

            # Latencia: Draft + Verificación
            self.total_latency += device.draft_token_time + self.verifier_step_time
            
            # Generación
            round_accepted = 0
            round_rejected = 0
            
            for _ in range(self.speculative_window):
                if total_generated + round_accepted + round_rejected >= self.config.maxResponseLength:
                    break
                    
                if random.random() < device.accuracypredcttion:
                    round_accepted += 1
                else:
                    round_rejected += 1
                    break
            
            if round_rejected > 0:
                round_accepted += 1
            
            print(f"  -> Accepted: {round_accepted} | Rejected: {round_rejected}")
            
            self.accepted_tokens += round_accepted
            self.rejected_tokens += round_rejected
            total_generated += (round_accepted + round_rejected)
            
            print(f"  -> Progress: {total_generated}/{self.config.maxResponseLength} | Latency: {self.total_latency:.4f}")
            print("-" * 40)
            
            round_number += 1
        
    def run(self) -> SimulationResult:
        total_generated = 0
        round_number = 0
        print(f"\n--- Starting Simulation ---")
        
        while total_generated < self.config.maxResponseLength:
            actual_round = round_number % 4
            if actual_round == 0: activos = [self.devices[0], self.devices[2]]
            elif actual_round == 1: activos = [self.devices[1]]
            elif actual_round == 2: activos = [self.devices[0], self.devices[1], self.devices[2]]
            else: activos = self.devices

    
            device = random.choice(activos)
            max_time = max(d.draft_token_time for d in activos)
            round_latency = max_time + self.verifier_step_time
            
            round_accepted = 0
            round_rejected = 0
            for _ in range(self.speculative_window):
                if total_generated + round_accepted + round_rejected >= self.config.maxResponseLength:
                    break
                if random.random() < device.accuracypredcttion:
                    round_accepted += 1
                else:
                    round_rejected += 1
                    break
            
            if round_rejected > 0: round_accepted += 1
            
            # 3. Calcular Arrival Time y sumar Latencia total
            draft_size = round_accepted + round_rejected
            #Delay assigned
            delay = 0.5
            arrival_time = (draft_size * device.draft_token_time) + delay
            
            self.total_latency += round_latency
        
            self.accepted_tokens += round_accepted
            self.rejected_tokens += round_rejected
            total_generated += draft_size
            
            print(f"Round {round_number} | Device: {device.device_id} | Arrival: {arrival_time:.4f} | Round Latency: {round_latency:.4f}")
            round_number += 1
    
        baseline_latency = self.config.maxResponseLength * 1.0 
        speedup = baseline_latency / self.total_latency if self.total_latency > 0 else 0
        print(f"Verifier Calls: {len(self.devices) * round_number}")
        print(f"Draft Calls: {round_number}")
        print(f"Total latency: {self.total_latency:.2f}")
        print(f"Speedup: {speedup:.2f}x")
        
        return SimulationResult(
            accuracy=self.accepted_tokens / (self.accepted_tokens + self.rejected_tokens) if (self.accepted_tokens + self.rejected_tokens) > 0 else 0,
            latency=self.total_latency,
            numOfAcceptedTokens=self.accepted_tokens,
            numOfRejectedTokens=self.rejected_tokens,
            num_devices=len(self.devices),
            is_async=self.config.is_async
        )

def main():
    devices = [
        EdgeDevice(device_id="Edge_A", draft_token_time=0.8, accuracypredcttion=0.9, numberOftokensGenerated=4),
        EdgeDevice(device_id="Edge_B", draft_token_time=0.2, accuracypredcttion=0.7, numberOftokensGenerated=3),
        EdgeDevice(device_id="Edge_C", draft_token_time=0.3, accuracypredcttion=0.85, numberOftokensGenerated=3)
    ]
    config = SimulationConfig(num_devices=3, is_async=False, device_ids=["A", "B", "C"], maxResponseLength=20)

    sim = Simulator(config, devices, speculative_window=5, verifier_step_time=0.05)
    sim.run()

if __name__ == "__main__":
    main()


