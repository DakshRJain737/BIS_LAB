import random

n = int(input("Enter number of cities: "))

dist = []
print("Enter distance matrix:")
for _ in range(n):
    dist.append(list(map(int, input().split())))

POP_SIZE = 6
GENERATIONS = 3
MUTATION_RATE = 0.2


def fitness(route):
    return sum(dist[route[i]][route[(i + 1) % n]] for i in range(n))


def crossover(p1, p2):
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[a:b] = p1[a:b]

    remaining = [x for x in p2 if x not in child]
    j = 0

    for i in range(n):
        if child[i] is None:
            child[i] = remaining[j]
            j += 1

    return child


def mutate(route):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(n), 2)
        route[i], route[j] = route[j], route[i]


# Initial population
population = []

for _ in range(POP_SIZE):
    route = list(range(n))
    random.shuffle(route)
    population.append(route)

print("\nInitial Population:")

for route in population:
    print(route, "=", fitness(route))


# Genetic Algorithm
for gen in range(1, GENERATIONS + 1):

    population.sort(key=fitness)

    # Selection
    selected = population[:POP_SIZE // 2]

    new_population = selected.copy()

    # Crossover + Mutation
    while len(new_population) < POP_SIZE:
        p1, p2 = random.sample(selected, 2)

        child = crossover(p1, p2)
        mutate(child)

        new_population.append(child)

    population = new_population

    best = min(population, key=fitness)

    print("\nGeneration", gen)
    print("Best Route =", best)
    print("Distance =", fitness(best))


# Final result
best = min(population, key=fitness)

print("\nFinal Result:")
print("Best Route:", " -> ".join(map(str, best + [best[0]])))
print("Minimum Distance:", fitness(best))
