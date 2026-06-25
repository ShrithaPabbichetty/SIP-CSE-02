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
    while numOfTokensGenerated < response_length:
        if random.random() < device.accuracypredcttion:
            accepted += 1
            numOfTokensGenerated += 1
        else:
            rejected += 1
            break 

    return accepted, rejected
    
  
            


def simulateResponse (device, numOfTokensGenerated, response_length):
    while response_length > numOfTokensGenerated:
        accepted, rejected = simulateRound(device, numOfTokensGenerated, response_length)
        print("")
        print(response_length)
        print(numOfTokensGenerated)
        #response_length -= accepted
        if rejected > 0:
            numOfTokensGenerated += 1
    
    latency = device.draft_token_time * (numOfTokensGenerated)
    return SimulationResult(
        latency=latency,
        accuracy=device.accuracypredcttion,
        numOfAcceptedTokens=accepted,
        numOfRejectedTokens=rejected,
        num_devices=1,
        is_async=False

    )

def main(): 
    device = EdgeDevice(device_id="device_1", draft_token_time=0.5, accuracypredcttion=0.8, numberOftokensGenerated=10)
    response_length = 5
    draft_size = 3

    result = simulateResponse(device, draft_size, response_length)
    print(result)


if __name__ == "__main__":
    main()
