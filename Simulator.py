from simulationOutputMetrics import SimulationResult
from edgeDevice import EdgeDevice
import random 

def baselineMetrics (response_length, token_time):
    return SimulationResult(
        latency=token_time * response_length,
        accuracy=None,
        numOfAcceptedTokens=response_length,
        numOfRejectedTokens=0,
        num_devices= 1,
        is_async=False
    )



def simulateRound (device, tokensRemaining):
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
    
  
            


def simulateResponse (device, response_length):
    totalaccepted, totalrejected, totalGenerated = 0, 0, 0
    while totalGenerated < response_length:
        accepted, rejected = simulateRound(device, response_length - totalGenerated)
        totalaccepted += accepted
        totalrejected += rejected
        totalGenerated += (accepted + rejected)
        print("")
        print(response_length)
        print(totalGenerated)

    
    latency = device.draft_token_time * (totalGenerated)
    return SimulationResult(
        latency=latency,
        accuracy=device.accuracyprediction,
        numOfAcceptedTokens=totalaccepted,
        numOfRejectedTokens=totalrejected,
        num_devices=1,
        is_async=False

    )

def simulateMultiDeviceResponse (devices, response_length, communication_times):
    totalaccepted, totalrejected, totalGenerated = 0, 0, 0
    totalLatency = 0.0
    deviceIndex = 0

    while totalGenerated < response_length:
        device = devices[deviceIndex % len(devices)]
        delay = communication_times[deviceIndex % len(communication_times)]
        tokensRemaining = response_length - totalGenerated
        accepted, rejected = simulateRound(device, tokensRemaining)

        tokensAttempted = accepted + rejected
        roundLatency = delay * 2 + device.draft_token_time * tokensAttempted
        totalLatency += roundLatency

        if rejected > 0:
            tokensAdvanced = min(accepted+1, tokensRemaining)
        else:
            tokensAdvanced = min(accepted, tokensRemaining)

        totalaccepted += accepted
        totalrejected += rejected
        totalGenerated += tokensAdvanced

        print(
            f"Device {device.device_id} generated {tokensAttempted} tokens, "
            f"accepted: {accepted}, "
            f"rejected: {rejected}, "
            f"advanced: {tokensAdvanced}, "
            f"totalGenerated: {totalGenerated}/{response_length}, "
            f"roundLatency: {roundLatency:.2f}s, "
            f"totalLatency: {totalLatency:.2f}s"
        )
            
        
        deviceIndex += 1
    
    totalAccuracy = 0
    for i in devices:
        totalAccuracy += i.accuracyprediction
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
    device = EdgeDevice(device_id="device_1", draft_token_time=0.5, accuracyprediction=0.8, numberOftokensGenerated=10, communication_time = 0.1)

    device2 = EdgeDevice(device_id="device-2", draft_token_time=0.8, accuracyprediction=0.9, numberOftokensGenerated=4, communication_time = 0.2)
    device3 = EdgeDevice(device_id="device-3", draft_token_time=0.2, accuracyprediction=0.7, numberOftokensGenerated=3, communication_time = 0.3)
    device4 = EdgeDevice(device_id="device-4", draft_token_time=0.3, accuracyprediction=0.85, numberOftokensGenerated=3, communication_time = 0.4)
    communication_times = [device.communication_time, device2.communication_time, device3.communication_time]

    response_length = 10


    print("Simulating single device response:")
    result = simulateResponse(device, response_length)
    print(result)

    print("\nSimulating multi-device response:")
    multi_device_result = simulateMultiDeviceResponse([device, device2, device3, device4], response_length, communication_times)
    print(multi_device_result)


if __name__ == "__main__":
    main()
