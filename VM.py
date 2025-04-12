import random
import matplotlib.pyplot as plt


def fitness_function(chromosomes):
    scores = len(chromosomes) * [0]
    VM = {1: 2, 2: 4, 3: 8, 4: 2, 5: 6, 6: 4, 7: 10, 8: 8, 9: 6, 10: 2}
    for i in range(len(chromosomes)):
        Remaining_Space = {1: 16, 2: 16, 3: 16, 4: 16, 5: 16}
        exceedLimit = False
        chromosome = chromosomes[i]
        for j in range(len(chromosome)):
            if VM[j + 1] > Remaining_Space[chromosome[j]]:
                scores[i] = -1
                exceedLimit = True
                break
            else:
                Remaining_Space[chromosome[j]] -= VM[j + 1]
        if exceedLimit:
            continue
        for value in Remaining_Space.values():
            if value == 16:
                scores[i] += 1.2
            elif value == 0:
                scores[i] += 1
    return [(scores[i]) for i in range(len(chromosomes))]


def tournament_selection(chromosomes, fitnesses, k=2):
    parents = []
    for _ in range(len(chromosomes)):
        tournament = random.sample(range(len(chromosomes)), k)
        best = max(tournament, key=fitnesses.__getitem__)
        parents.append(chromosomes[best])
    return parents


def one_point_crossover(parents):
    children = []
    for i in range(0, len(parents), 2):
        p1 = parents[i]
        p2 = parents[i + 1]
        point = random.randint(1, len(p1) - 1)
        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]
        children.extend([c1, c2])
    return children

def two_point_crossover(parents):
    children = []
    for i in range(0, len(parents), 2):
        p1 = parents[i]
        p2 = parents[i + 1]
        point1 = random.randint(0, len(p1) - 2)
        point2 = random.randint(point1 + 1, len(p1) - 1)
        c1 = p1[:point1] + p2[point1:point2] + p1[point2:]
        c2 = p2[:point1] + p1[point1:point2] + p2[point2:]
        children.extend([c1, c2])
    return children


chromosomes = []
for _ in range(50):
    chromosome = [random.randint(1, 5) for _ in range(10)]
    chromosomes.append(chromosome)

best_fitness = max(fitness_function(chromosomes))
best_chromosome = []
fitness_progress = []

for generation in range(100):
    fitnesses = fitness_function(chromosomes)
    parents = tournament_selection(chromosomes, fitnesses)
    max_fitness = max(fitnesses)
    best_fitness = max(best_fitness, max_fitness)
    fitness_progress.append(best_fitness)
    if best_fitness == max_fitness:
        index = fitnesses.index(max_fitness)
        best_chromosome = chromosomes[index]
    #هر دو پیاده سازی شده اند
    children = one_point_crossover(parents)
    # children = two_point_crossover(parents)

    for child in children:
        if random.random() < 0.2:
            index = random.randint(0, 9)
            old_pm = child[index]
            new_pm = random.randint(1, 5)
            while new_pm == old_pm:
                new_pm = random.randint(1, 5)
            child[index] = new_pm

    chromosomes = children


print("Best chromosome:", best_chromosome)
print("Best fitness:", best_fitness)

plt.figure(figsize=(10, 5))
plt.plot(fitness_progress, label="Best Fitness", color="orange")
plt.xlabel("Generation")
plt.ylabel("Best Fitness")
plt.title("Best Fitness Over Generations")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

VM = {1: 2, 2: 4, 3: 8, 4: 2, 5: 6, 6: 4, 7: 10, 8: 8, 9: 6, 10: 2}
PM_labels = {1: "PM1", 2: "PM2", 3: "PM3", 4: "PM4", 5: "PM5"}

pm_bars = {1: [], 2: [], 3: [], 4: [], 5: []}
current_time = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

for vm_index, pm in enumerate(best_chromosome):
    vm_id = vm_index + 1
    duration = VM[vm_id]
    start = current_time[pm]
    end = start + duration
    pm_bars[pm].append((start, duration, f"VM{vm_id}"))
    current_time[pm] = end

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['red', 'green', 'blue', 'orange', 'purple']
for i, pm in enumerate(pm_bars.keys()):
    for bar in pm_bars[pm]:
        ax.barh(y=i, width=bar[1], left=bar[0], height=0.6, align='center', color=colors[i], edgecolor='black')
        ax.text(bar[0] + bar[1] / 2, i, bar[2], va='center', ha='center', color='white', fontsize=8)

ax.set_yticks(range(5))
ax.set_yticklabels([PM_labels[pm] for pm in pm_bars.keys()])
ax.set_xlabel("Size")
ax.set_title("Gantt Chart of VM Allocations in Best Chromosome")
plt.grid(True)
plt.tight_layout()
plt.show()
