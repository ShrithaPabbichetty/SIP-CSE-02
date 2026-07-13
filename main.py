

from simulationOutputMetrics import SimulationResult
from edgeDevice import EdgeDevice
from simulationInputMetrics import SimulationConfig
from Simulator import MultiEdgeSpeculativeSimulator
from plot import plot_results, plot_bar_results
import random

def select_fastest_devices(devices, top_n=2):
    def calculate_total_latency(device):
        return (device.draft_token_time * device.number_of_tokens_generated) + device.communication_time
   
    sorted_devices = sorted(devices, key=calculate_total_latency)
    return sorted_devices[:top_n]


def main():
   device1 = EdgeDevice(device_id="device-1", draft_token_time=5.6, accuracy=0.9, number_of_tokens_generated=10, communication_time=6.7)
   device2 = EdgeDevice(device_id="device-2", draft_token_time=9.2, accuracy=0.9, number_of_tokens_generated=4, communication_time=3.3)
   device3 = EdgeDevice(device_id="device-3", draft_token_time=6.2, accuracy=0.9, number_of_tokens_generated=3, communication_time=3.1)
   device4 = EdgeDevice(device_id="device-4", draft_token_time=7.1, accuracy=0.9, number_of_tokens_generated=3, communication_time=2.8)


   devices = [device1, device2, device3, device4]

   #round robin schedule
   '''random.shuffle(devices)

   n = len(devices)
   round_schedule = []
   for i in range(n):
       round_schedule.append([devices[i], devices[(i + 1) % n]])
   
   print("Round schedule:")
   for i, rnd in enumerate(round_schedule, 1):
       print(f"Round {i}: {[d.device_id for d in rnd]}")'''
   
   # highest accuracy schedule
   sorted_devices = sorted(devices, key=lambda d: d.accuracy, reverse=True)
   top_two = sorted_devices[:2]

   round_schedule = [
       top_two,  # Round 1: Top two devices
   ]

   # random 
   '''round_schedule = [
      random.sample(devices, 2)
      for _ in range(20)
   ]'''

   # least latency schedule
   '''round_schedule = select_fastest_devices(devices, top_n=2)'''


   config = SimulationConfig(
       num_devices=len(devices),
       is_async=True,
       device_ids=devices,
       response_length=10,
       target_token_time=40,
       verifier_time=30,
       speculative_window=3,
       seed=random.randint(1, 1000),
       round_schedule=round_schedule
   )


   sim = MultiEdgeSpeculativeSimulator(config)


   baseline = sim.run_baseline()
   print("Baseline latency:", baseline.latency)


   print("\nSimulating multi-device response:")
   multi_result = sim.run()
   print(multi_result)


   speedup = baseline.latency / multi_result.latency
   print("\nSpeedup of multi-device over baseline:", round(speedup, 2))


   # ---- Draft Accuracy latency data (avg / min / max) ----
   #avg_1 = [283.54, 268.86, 232.0, 239.5, 202.8]
   #min_1 = [239.5, 202.8, 202.0, 202.8, 202.8]
   #max_1 = [312.9, 349.6, 312.9, 276.2, 202.8]


   #avg_2 = [423.44, 358.398, 296.02, 289.798, 310.438]
   #min_2 = [282.3, 278.7, 227.0, 225.2, 225.2]
   #max_2 = [524.2, 422.79, 332.2, 352.7, 439.19]


   #avg_3 = [470.44, 437.82, 330.76, 312.64, 294.92]
   #min_3 = [411.6, 372.9, 227.0, 271.3, 271.3]
   #max_3 = [519.8, 542.6, 391.3, 393.1, 323.0]


   yerr_list_accuracy = [
       [[a - lo for a, lo in zip(avg_1, min_1)], [hi - a for a, hi in zip(avg_1, max_1)]],
       [[a - lo for a, lo in zip(avg_2, min_2)], [hi - a for a, hi in zip(avg_2, max_2)]],
       [[a - lo for a, lo in zip(avg_3, min_3)], [hi - a for a, hi in zip(avg_3, max_3)]],
   ]

   # Plot Draft Accuracy vs Latency for 1, 2, and 3 devices
   plot_results(
       xpoints=[
           [0.5, 0.6, 0.7, 0.8, 0.9],
       ],
       y_list=[
           avg_1,
           avg_2,
           avg_3,
       ],
       xlabel="Draft Accuracy",
       ylabel="Latency",
       colors=["blue", "red", "green"],
       labels=["1 Device", "2 Devices", "3 Devices"],
       line_style=["-", "--", "-."],
       marker=["o", "s", "^"],
       yerr_list=yerr_list_accuracy
   )


   # Communication Time latency data (avg / min / max)
   avg_fast = [260.56, 269.64, 267.84, 316.84, 342.44]
   min_fast = [221.4, 231.4, 241.4, 256.4, 232.6]
   max_fast = [325.8, 330.4, 304.4, 416.6, 444.4]


   avg_mixed = [302.48, 290.34, 299.92, 333.98, 388.5]
   min_mixed = [247.3, 212.7, 215.4, 227.4, 292.2]
   max_mixed = [337.6, 351.6, 365.6, 391.0, 507.1]


   avg_all = [383.68, 391.4, 424.82, 464.44, 433.72]
   min_all = [298.2, 328.5, 332.2, 414.5, 362.5]
   max_all = [504.5, 441.2, 543.8, 521.7, 487.5]


   yerr_list_comm = [
       [[a - lo for a, lo in zip(avg_fast, min_fast)], [hi - a for a, hi in zip(avg_fast, max_fast)]],
       [[a - lo for a, lo in zip(avg_mixed, min_mixed)], [hi - a for a, hi in zip(avg_mixed, max_mixed)]],
       [[a - lo for a, lo in zip(avg_all, min_all)], [hi - a for a, hi in zip(avg_all, max_all)]],
   ]

   # Plot Communication Time vs Total Latency for fast, mixed, and all device groups
   plot_results(
       xpoints=[1, 3, 5, 8, 10],
       y_list=[
           avg_fast,
           avg_mixed,
           avg_all,
       ],
       xlabel="Communication Time",
       ylabel="Latency",
       colors=["blue", "red", "green"],
       labels=["Fast Devices", "Mixed Devices", "All Devices"],
       line_style=["-", "--", "-."],
       marker=["o", "s", "^"],
       yerr_list=yerr_list_comm
   )


x_devices = [1, 2, 3, 4]


#Low
avg_low = [196.76, 252.5598, 338.796, 382.576]
min_low = [183.9, 199.1, 299.2, 323.79]
max_low = [216.0, 305.9, 394.9, 479.3]


# Medium
avg_medium = [209.998, 305.676, 366.76, 405.06]
min_medium = [195.99, 230.39, 269.2, 333.8]
max_medium = [231, 359.8, 479.8, 505.3]


# High
avg_high = [217.7, 307.56, 361.1, 444.86]
min_high = [210.0, 284.5, 287.7, 365.6]
max_high = [248.5, 336.6, 411.1, 578.6]


yerr_low = [
   [a - lo for a, lo in zip(avg_low, min_low)],
   [hi - a for a, hi in zip(avg_low, max_low)],
]


yerr_medium = [
   [a - lo for a, lo in zip(avg_medium, min_medium)],
   [hi - a for a, hi in zip(avg_medium, max_medium)],
]


yerr_high = [
   [a - lo for a, lo in zip(avg_high, min_high)],
   [hi - a for a, hi in zip(avg_high, max_high)],
]


# Plot Latency vs Number of Selected Devices comparing communication conditions
plot_results(
   xpoints=x_devices,
   y_list=[
       avg_low,
       avg_medium,
       avg_high,
   ],
   xlabel="Number of Selected Devices",
   ylabel="Latency",
   colors=["blue", "red", "green"],
   labels=[
       "Low Communication",
       "Medium Communication",
       "High Communication",
   ],
   line_style=["dashed", "dotted", "dashdot"],
   marker=["o", "s", "^"],
   yerr_list=[
       yerr_low,
       yerr_medium,
       yerr_high,
   ],
)


x_verifier = [20, 30, 40, 50, 60]


# Low draft accuracy .6
avg_low = [1.40, 1.04, 0.98, 0.78, 0.72]
min_low = [1.0, 0.8, 0.8, 0.6, 0.6]
max_low = [2.2, 1.3, 1.2, 1.0, 0.8]


# Medium draft accuracy .8
avg_medium = [1.76, 1.48, 1.44, 1.06, 0.96]
min_medium = [1.3, 1.2, 1.3, 0.8, 0.7]
max_medium = [2.2, 1.8, 1.6, 1.4, 1.2]


# High draft accuracy .9
avg_high = [2.16, 1.74, 1.40, 1.12, 1.06]
min_high = [1.9, 1.5, 1.2, 0.8, 0.8]
max_high = [2.3, 1.8, 1.5, 1.3, 1.2]


yerr_low = [
   [a - lo for a, lo in zip(avg_low, min_low)],
   [hi - a for a, hi in zip(avg_low, max_low)],
]


yerr_medium = [
   [a - lo for a, lo in zip(avg_medium, min_medium)],
   [hi - a for a, hi in zip(avg_medium, max_medium)],
]


yerr_high = [
   [a - lo for a, lo in zip(avg_high, min_high)],
   [hi - a for a, hi in zip(avg_high, max_high)],
]


plot_results(
   xpoints=x_verifier,
   y_list=[
       avg_low,
       avg_medium,
       avg_high,
   ],
   xlabel="Verifier Time",
   ylabel="Speedup vs Baseline",
   colors=["blue", "red", "green"],
   labels=[
       "Draft Accuracy = 0.6",
       "Draft Accuracy = 0.8",
       "Draft Accuracy = 0.9",
   ],
   line_style=["-", "--", "-."],
   marker=["o", "s", "^"],
   yerr_list=[
       yerr_low,
       yerr_medium,
       yerr_high,  
   ],
  
)

# Latency vs Draft Accuracy

x_accuracy = [0.5, 0.6, 0.7, 0.8, 0.9]

# Round Robin
avg_rr = [476.42, 410.54, 392.86, 291.34, 248.36]
min_rr = [437.7, 284.6, 294.4, 242.7, 239.4]
max_rr = [507.6, 499.4, 482.9, 354.6, 253.3]

# Least Latency
avg_ll = [368.42, 287.86, 292.74, 224.94, 224.78]
min_ll = [334.6, 245.3, 286.7, 202.2, 202.2]
max_ll = [415.2, 368.2, 299.4, 254.8, 249.2]

# Random
avg_random = [401.22, 381.78, 328.42, 319.30, 239.94]
min_random = [322.2, 300.2, 278.9, 270.2, 220.9]
max_random = [452.4, 474.1, 360.7, 387.3, 276.4]

yerr_random = [
    [a - lo for a, lo in zip(avg_random, min_random)],
    [hi - a for a, hi in zip(avg_random, max_random)],
]

yerr_rr = [
    [a - lo for a, lo in zip(avg_rr, min_rr)],
    [hi - a for a, hi in zip(avg_rr, max_rr)],
]

yerr_ll = [
    [a - lo for a, lo in zip(avg_ll, min_ll)],
    [hi - a for a, hi in zip(avg_ll, max_ll)],
]

# Plot Latency vs Draft Accuracy comparing scheduling policies
plot_results(
    xpoints=x_accuracy,
    y_list=[
        avg_rr,
        avg_ll,
        avg_random,
    ],
    xlabel="Draft Accuracy",
    ylabel="Latency",
    colors=["blue", "red", "green"],
    labels=[
        "Round Robin",
        "Least Latency",
        "Random"
    ],
    line_style=["-", "--", "-."],
    marker=["o", "s", "^"],
    yerr_list=[
        yerr_rr,
        yerr_ll,
        yerr_random
    ],
)

# Latency vs Communication Time

x_comm = [1, 3, 5, 8, 10]

# Round Robin
avg_rr = [270.10, 293.78, 301.08, 339.68, 363.20]
min_rr = [246.1, 254.6, 273.6, 286.7, 285.9]
max_rr = [309.8, 367.3, 314.3, 396.2, 480.5]

# Highest Accuracy
avg_ha = [225.46, 255.92, 272.14, 307.22, 317.46]
min_ha = [195.0, 207.1, 241.2, 225.6, 287.8]
max_ha = [279.0, 293.8, 303.0, 388.1, 386.8]

# Least Latency
avg_ll = [297.42, 322.12, 340.54, 389.84, 439.40]
min_ll = [278.3, 251.9, 218.1, 313.2, 396.2]
max_ll = [321.7, 390.0, 441.8, 473.3, 482.4]

# Random
avg_rand = [325.66, 289.48, 342.76, 338.98, 352.94]
min_rand = [252.7, 220.8, 270.6, 290.4, 250.4]
max_rand = [366.8, 326.8, 421.3, 447.3, 455.0]

yerr_rr = [
    [a - lo for a, lo in zip(avg_rr, min_rr)],
    [hi - a for a, hi in zip(avg_rr, max_rr)],
]

yerr_ha = [
    [a - lo for a, lo in zip(avg_ha, min_ha)],
    [hi - a for a, hi in zip(avg_ha, max_ha)],
]

yerr_ll = [
    [a - lo for a, lo in zip(avg_ll, min_ll)],
    [hi - a for a, hi in zip(avg_ll, max_ll)],
]

yerr_rand = [
    [a - lo for a, lo in zip(avg_rand, min_rand)],
    [hi - a for a, hi in zip(avg_rand, max_rand)],
]

# Plot Latency vs Communication Time comparing scheduling policies
plot_results(
    xpoints=x_comm,
    y_list=[
        avg_rr,
        avg_rand,
        avg_ll,
        avg_ha,
    ],
    xlabel="Communication Time",
    ylabel="Latency",
    colors=["blue", "orange", "red", "green"],
    labels=[
        "Round Robin",
        "Random",
        "Least Latency",
        "Highest Accuracy",
    ],
    line_style=["-", "--", "-.", ":"],
    marker=["o", "s", "^", "d"],
    yerr_list=[
        yerr_rr,
        yerr_rand,
        yerr_ll,
        yerr_ha,
    ],
)

# Scheduler Comparison (Bar Chart)

scheduler_labels = [
    "Round Robin",
    "Random",
    "Least Latency",
    "Highest Accuracy",
]

avg_latency = [
    317.92,
    328.94,
    267.72,
    239.28,
]

yerr = [
    [317.92 - 263.9, 328.94 - 215.8, 267.72 - 207.8, 239.28 - 209.6],
    [408.2 - 317.92, 416.8 - 328.94, 344.9 - 267.72, 351.8 - 239.28],
]

# Plot scheduler comparison as a bar chart
plot_bar_results(
    labels=scheduler_labels,
    values=avg_latency,
    xlabel="Scheduling Policy",
    ylabel="Average Latency",
    title="Scheduler Comparison",
    colors=["blue", "orange", "green", "red"],
    yerr=yerr,
)

#Latency vs Number of Selected Devices

x_devices = [1, 2, 3, 4]

#Random
avg_random = [286.24, 283.72, 351.58, 332.92]
min_random = [225.6, 233.6, 225.7, 310.9]
max_random = [324.8, 332.0, 463.0, 346.2]

#Round Robin
avg_rr = [343.68, 282.32, 353.08, 360.8]
min_rr = [264.0, 224.4, 332.7, 325.4]
max_rr = [429.6, 315.0, 387.0, 400.1]

#Highest Accuracy
avg_ha = [213.44, 291.8, 324.36, 284.0]
min_ha = [187.2, 215.2, 224.4, 224.4]
max_ha = [252.8, 337.0, 400.0, 431.8]

#Least Latency
avg_ll = [202.8, 294.9, 362.96, 299.84]
min_ll = [202.8, 236.2, 316.2, 256.3]
max_ll = [202.8, 332.2, 398.2, 339.3]

# Error bars
yerr_random = [
    [a - lo for a, lo in zip(avg_random, min_random)],
    [hi - a for a, hi in zip(avg_random, max_random)],
]

yerr_rr = [
    [a - lo for a, lo in zip(avg_rr, min_rr)],
    [hi - a for a, hi in zip(avg_rr, max_rr)],
]

yerr_ha = [
    [a - lo for a, lo in zip(avg_ha, min_ha)],
    [hi - a for a, hi in zip(avg_ha, max_ha)],
]

yerr_ll = [
    [a - lo for a, lo in zip(avg_ll, min_ll)],
    [hi - a for a, hi in zip(avg_ll, max_ll)],
]

plot_results(
    xpoints=x_devices,
    y_list=[
        avg_random,
        avg_rr,
        avg_ha,
        avg_ll,
    ],
    xlabel="Number of Selected Devices",
    ylabel="Latency",
    colors=[
        "green",
        "blue",
        "red",
        "purple",
    ],
    labels=[
        "Random",
        "Round Robin",
        "Highest Accuracy",
        "Least Latency",
    ],
    line_style=[
        "-.",
        "-",
        "--",
        ":",
    ],
    marker=[
        "^",
        "o",
        "s",
        "d",
    ],
    yerr_list=[
        yerr_random,
        yerr_rr,
        yerr_ha,
        yerr_ll,
    ],
)

#Async vs Sync: Latency vs Communication Time

x_comm = [1, 3, 5, 8, 10]

# Async
avg_async = [207.5, 224.0, 249.8, 265.7, 259.6]
min_async = [180, 188.0, 199.0, 211.0, 217.5]
max_async = [215.5, 291.5, 272.0, 290.0, 302.0]

# Sync
avg_sync = [225.46, 255.92, 272.14, 307.22, 317.46]
min_sync = [195.0, 207.1, 241.2, 225.6, 287.8]
max_sync = [279.0, 293.8, 303.0, 388.1, 386.8]

yerr_async = [
    [a - lo for a, lo in zip(avg_async, min_async)],
    [hi - a for a, hi in zip(avg_async, max_async)],
]

yerr_sync = [
    [a - lo for a, lo in zip(avg_sync, min_sync)],
    [hi - a for a, hi in zip(avg_sync, max_sync)],
]

plot_results(
    xpoints=x_comm,
    y_list=[
        avg_async,
        avg_sync,
    ],
    xlabel="Communication Time",
    ylabel="Latency",
    colors=["blue", "red"],
    labels=[
        "Async",
        "Sync",
    ],
    line_style=["-", "--"],
    marker=["o", "s"],
    yerr_list=[
        yerr_async,
        yerr_sync,
    ],
)

#Sync vs Async at a Fixed Setting (Highest Accuracy)

labels = ["Sync", "Async"]

avg_latency = [
    279.84,
    217.02,
]

yerr = [
    [
        279.84 - 195.0,
        217.02 - 195.0,
    ],
    [
        332.8 - 279.84,
        245.4 - 217.02,
    ],
]

plot_bar_results(
    labels=labels,
    values=avg_latency,
    xlabel="Execution Mode",
    ylabel="Latency",
    title="Sync vs Async at a Fixed Setting (Highest Accuracy)",
    colors=["steelblue", "orange"],
    yerr=yerr,
)

#Async vs Sync: Latency vs Number of Selected Devices

x_devices = [1, 2, 3, 4]

# Async
avg_async = [255.86, 225.24, 220.32, 230.84]
min_async = [195.0, 195.0, 202.1, 195.0]
max_async = [325.7, 245.4, 249.9, 286.1]

# Sync
avg_sync = [286.24, 283.72, 351.58, 332.92]
min_sync = [225.6, 233.6, 225.7, 310.9]
max_sync = [324.8, 332.0, 463.0, 346.2]

yerr_async = [
    [a - lo for a, lo in zip(avg_async, min_async)],
    [hi - a for a, hi in zip(avg_async, max_async)],
]

yerr_sync = [
    [a - lo for a, lo in zip(avg_sync, min_sync)],
    [hi - a for a, hi in zip(avg_sync, max_sync)],
]

plot_results(
    xpoints=x_devices,
    y_list=[
        avg_async,
        avg_sync,
    ],
    xlabel="Number of Selected Devices",
    ylabel="Latency",
    colors=["blue", "red"],
    labels=[
        "Async",
        "Sync",
    ],
    line_style=["-", "--"],
    marker=["o", "s"],
    yerr_list=[
        yerr_async,
        yerr_sync,
    ],
)

# ---- Scheduler Comparison (Async Mode) ----

labels = [
    "Least Latency",
    "Round Robin",
    "Random",
    "Highest Accuracy",
]

avg_latency = [
    222.4,
    228.0,
    264.82,
    250.04,
]

yerr = [
    [
        222.4 - 197.6,
        228.0 - 197.6,
        264.82 - 231.2,
        250.04 - 197.6,
    ],
    [
        288.0 - 222.4,
        279.0 - 228.0,
        289.5 - 264.82,
        326.8 - 250.04,
    ],
]

plot_bar_results(
    labels=labels,
    values=avg_latency,
    xlabel="Scheduling Policy",
    ylabel="Latency",
    title="Scheduler Comparison (Async Mode)",
    colors=["red", "blue", "orange", "green"],
    yerr=yerr,
)

# ---- Sync vs Async (Highest Accuracy): Latency vs Draft Accuracy ----

x_accuracy = [0.5, 0.6, 0.7, 0.8, 0.9]

# Async
avg_async = [323.64, 313.94, 278.60, 291.56, 219.84]
min_async = [284.0, 276.4, 202.8, 254.4, 202.8]
max_async = [354.2, 350.0, 349.8, 343.6, 243.5]

# Sync
avg_sync = [229.7285714, 229.3428571, 222.5142857, 225.5571429, 212.1714286]
min_sync = [202.1, 195.0, 195.0, 195.0, 195.0]
max_sync = [280.9, 281.6, 245.4, 249.9, 245.4]

yerr_async = [
    [a - lo for a, lo in zip(avg_async, min_async)],
    [hi - a for a, hi in zip(avg_async, max_async)],
]

yerr_sync = [
    [a - lo for a, lo in zip(avg_sync, min_sync)],
    [hi - a for a, hi in zip(avg_sync, max_sync)],
]

plot_results(
    xpoints=x_accuracy,
    y_list=[
        avg_sync,
        avg_async,
    ],
    xlabel="Draft Accuracy",
    ylabel="Latency",
    colors=["blue", "red"],
    labels=[
        "Sync",
        "Async",
    ],
    line_style=["-", "--"],
    marker=["o", "s"],
    yerr_list=[
        yerr_sync,
        yerr_async,
    ],
)

if __name__ == "__main__":
   main()
