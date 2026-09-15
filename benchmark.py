import sys
import os
import random
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.algorithms import AlgorithmsEngine

PRIORITIES = ["low", "medium", "high"]

def make_tasks(n):
    return [
        {"id": i, "title": f"Task {i}", "priority": random.choice(PRIORITIES)}
        for i in range(n)
    ]

def run_benchmark():
    for n in [10, 500, 3000]:
        tasks = make_tasks(n)

        sorted_tasks, sort_comparisons = AlgorithmsEngine.insertion_sort_tasks_counted(tasks.copy())

        search_target = tasks[n // 2]["title"]
        _, linear_comparisons = AlgorithmsEngine.linear_search_counted(tasks, search_target)

        sorted_by_title = sorted(tasks, key=lambda x: x["title"].lower())
        _, binary_comparisons = AlgorithmsEngine.binary_search_counted(sorted_by_title, search_target)

        print(f"\n--- n = {n} ---")
        print(f"Insertion Sort comparisons: {sort_comparisons}")
        print(f"Linear Search comparisons:  {linear_comparisons}")
        print(f"Binary Search comparisons:  {binary_comparisons}")

if __name__ == "__main__":
    run_benchmark()