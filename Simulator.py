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



def simulateRound (device, numOfTokensGenerated, response_length):
    accepted = 0
    rejected = 0

    #for i in range(draft_size):
    while response_length > numOfTokensGenerated:
        if random.random() < device.accuracypredcttion:
            accepted += 1
            numOfTokensGenerated += 1
        else:
            rejected += 1
            break 

    return accepted, rejected, numOfTokensGenerated
    
  
            


def simulateResponse (device, numOfTokensGenerated, response_length):
    totalAccepted = 0
    totalRejected = 0
    while response_length > numOfTokensGenerated:
        accepted, rejected, numOfTokensGenerated = simulateRound(device, numOfTokensGenerated, response_length)
        totalAccepted += accepted
        totalRejected += rejected
        print("")
        print(response_length)
        print(numOfTokensGenerated)
        if rejected > 0:
            numOfTokensGenerated += 1
    
    latency = device.draft_token_time * (numOfTokensGenerated)
    return SimulationResult(
        latency=latency,
        accuracy=device.accuracypredcttion,
        numOfAcceptedTokens=totalAccepted,
        numOfRejectedTokens=totalRejected,
        num_devices=1,
        is_async=False
    )



def main(): 
    device = EdgeDevice(device_id="device_1", draft_token_time=0.5, accuracypredcttion=0.8, numberOftokensGenerated=10)
    response_length = 5

    result = simulateResponse(device, 0,response_length)
    print(result)


if __name__ == "__main__":
    main()