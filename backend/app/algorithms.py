from typing import List, Dict, Any

class AlgorithmsEngine:

    # ---------- 1. INSERTION SORT (priority ke hisaab se: high > medium > low) ----------
    @staticmethod
    def insertion_sort_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        priority_weights = {"high": 3, "medium": 2, "low": 1}
        tasks = tasks.copy()  # original list mutate na ho isliye

        for i in range(1, len(tasks)):
            key_task = tasks[i]
            key_weight = priority_weights.get(key_task.get("priority", "low"), 1)
            j = i - 1

            # Higher priority wale tasks ko aage laane ke liye shift karo
            while j >= 0 and priority_weights.get(tasks[j].get("priority", "low"), 1) < key_weight:
                tasks[j + 1] = tasks[j]
                j -= 1

            tasks[j + 1] = key_task

        return tasks

    # ---------- 2. LINEAR SEARCH (title mein substring match, case-insensitive) ----------
    @staticmethod
    def linear_search(tasks: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        query = query.lower()
        matched = []
        for task in tasks:
            if query in task.get("title", "").lower():
                matched.append(task)
        return matched

    # ---------- 3. BINARY SEARCH (sorted list mein exact/prefix title match) ----------
    @staticmethod
    def binary_search(sorted_tasks: List[Dict[str, Any]], target_title: str) -> Dict[str, Any] | None:
        """
        NOTE: Binary search ke liye list already title ke hisaab se sorted honi chahiye
        (alphabetically), warna result galat aayega.
        """
        target_title = target_title.lower()
        low, high = 0, len(sorted_tasks) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_title = sorted_tasks[mid].get("title", "").lower()

            if mid_title == target_title:
                return sorted_tasks[mid]
            elif mid_title < target_title:
                low = mid + 1
            else:
                high = mid - 1

        return None