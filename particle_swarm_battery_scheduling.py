import random

# Battery parameters
BATTERY_CAPACITY = 100
MIN_SOC = 20
MAX_SOC = 90

# 6 time slots
PRICE = [5, 8, 12, 15, 10, 6]

PARTICLES = 10
ITERATIONS = 50

W = 0.5
C1 = 1.5
C2 = 1.5


# Objective function
def fitness(schedule):
    soc = 50
    cost = 0
    penalty = 0

    for i in range(len(schedule)):
        power = schedule[i]

        # Update battery SOC
        soc += power

        # Energy cost
        cost += power * PRICE[i]

        # Security constraints
        if soc < MIN_SOC:
            penalty += (MIN_SOC - soc) * 100

        if soc > MAX_SOC:
            penalty += (soc - MAX_SOC) * 100

        # Limit charging/discharging
        if abs(power) > 20:
            penalty += (abs(power) - 20) * 100

    return cost + penalty


# Create particles
particles = []

for _ in range(PARTICLES):
    position = [random.uniform(-20, 20) for _ in PRICE]
    velocity = [random.uniform(-2, 2) for _ in PRICE]

    particles.append({
        "position": position,
        "velocity": velocity,
        "best": position[:],
        "best_value": fitness(position)
    })


# Global best
gbest = min(particles, key=lambda p: p["best_value"])
global_best = gbest["best"][:]
global_best_value = gbest["best_value"]


# PSO
for iteration in range(ITERATIONS):

    for particle in particles:

        for i in range(len(PRICE)):

            r1 = random.random()
            r2 = random.random()

            particle["velocity"][i] = (
                W * particle["velocity"][i]
                + C1 * r1 * (particle["best"][i] -
                             particle["position"][i])
                + C2 * r2 * (global_best[i] -
                             particle["position"][i])
            )

            particle["position"][i] += particle["velocity"][i]

            # Battery power limit
            particle["position"][i] = max(
                -20, min(20, particle["position"][i])
            )

        value = fitness(particle["position"])

        # Personal best
        if value < particle["best_value"]:
            particle["best"] = particle["position"][:]
            particle["best_value"] = value

        # Global best
        if value < global_best_value:
            global_best = particle["position"][:]
            global_best_value = value


# Result
print("Optimal Battery Schedule:")

for i, power in enumerate(global_best):
    if power > 0:
        action = "Charging"
    else:
        action = "Discharging"

    print(
        "Slot", i + 1,
        ":", round(power, 2),
        "kW -", action
    )

print("\nMinimum Cost:", round(global_best_value, 2))
