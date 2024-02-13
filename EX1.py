import pandas as pd
import numpy as np


data = pd.read_csv('27-124b.txt', sep=' ', names=['Distance', 'Weight'], skiprows=1)
def calculate_delivered_packages(data, K, M):
    max_packages_delivered = 0
    best_location = None
    for location in data['Distance']:
        distance_to_houses = np.minimum(np.abs(data['Distance'] - location), K - np.abs(data['Distance'] - location))
        deliverable = data[distance_to_houses <= M]
        packages_delivered = deliverable['Packages'].sum()
        if packages_delivered > max_packages_delivered:
            max_packages_delivered = packages_delivered
            best_location = location
    return max_packages_delivered, best_location

with open('27-124b.txt', 'r') as file:
    first_line = file.readline().strip().split()
    N, K, V, M = map(int, first_line)

data['Packages'] = np.ceil(data['Weight'] / V).astype(int)

print(calculate_delivered_packages(data, K, M))



