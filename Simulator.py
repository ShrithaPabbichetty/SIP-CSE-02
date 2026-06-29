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

    #for i in range(draft_size):
    while accepted < tokensRemaining:
        if random.random() < device.accuracypredcttion:
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
        accuracy=device.accuracypredcttion,
        numOfAcceptedTokens=totalaccepted,
        numOfRejectedTokens=totalrejected,
        num_devices=1,
        is_async=False

    )

def main(): 
    device = EdgeDevice(device_id="device_1", draft_token_time=0.5, accuracypredcttion=0.8, numberOftokensGenerated=10)
    response_length = 5

    result = simulateResponse(device, response_length)
    print(result)