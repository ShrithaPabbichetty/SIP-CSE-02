from simulationOutputMetrics import SimulationResult

def baselineMetrics (response_length, token_time):
    return SimulationResult(
        latency=token_time * response_length,
        accuracy=None,
        numOfAcceptedTokens=response_length,
        numOfRejectedTokens=0,
        num_devices= 1,
        is_async=False
    )