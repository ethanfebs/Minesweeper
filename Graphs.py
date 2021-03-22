import math

import matplotlib.pyplot as plt
import numpy as np

from Minesweeper import run_game as basic_minesweeper
from Minesweeper_Advanced import run_game as advanced_minesweeper

figure_save_path = "graphs/"
figure_size = (16 * 2/3, 6)

def graph(minesweeper_algorithm, fname, dim = 25, iterations = 100, starting_density = 0.1, ending_density = 0.9, density_step = 0.1):
    density_values = np.arange(starting_density, ending_density + density_step, density_step)
    print(density_values)
    success_rate_values = []

    for density_value in density_values:
        number_of_mines = math.floor(density_value * dim * dim)
        total_success = 0
        for i in range(iterations):
            total_success += (minesweeper_algorithm(dim, number_of_mines) / number_of_mines)
        success_rate_values.append(total_success / iterations)

    plt.figure(figsize = figure_size)
    plt.scatter(density_values, success_rate_values, label = "Mine Identification Success Rate", color = "indigo")
    plt.xlabel("Mine Density")
    plt.ylabel(f"Average Success Rate Across {iterations} Iterations")
    plt.locator_params(nbins = 10)
    plt.title(f"{fname} Success Rate as Density Increases")
    plt.legend(loc = "best")
    plt.grid()
    plt.savefig(f"{figure_save_path}{fname}.png")
    plt.show()

if __name__ == "__main__":
    graph(basic_minesweeper, "Basic Algorithm")
    graph(advanced_minesweeper, "Advanced Algorithm")