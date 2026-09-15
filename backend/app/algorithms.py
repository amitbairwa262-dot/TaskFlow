from typing import List, Dict, Any, Tuple

class AlgorithmsEngine:

    # ---------- 1. INSERTION SORT (priority ke hisaab se: high > medium > low) ----------
    @staticmethod
    def insertion_sort_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        priority_weights = {"high": 3, "medium": 2, "low": 1}

        for i in range(1, len(tasks)):
            key_task = tasks[i]
            key_weight = priority_weights.get(key_task.get("priority", "low"), 1)
            j = i - 1

            while j >= 0 and priority_weights.get(tasks[j].get("priority", "low"), 1) < key_weight:
                tasks[j + 1] = tasks[j]
                j -= 1

            tasks[j + 1] = key_task

        return tasks

    # ---------- 1b. COUNTING VERSION (benchmark ke liye comparisons count karta hai) ----------
    @staticmethod
    def insertion_sort_tasks_counted(tasks: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
        priority_weights = {"high": 3, "medium": 2, "low": 1}
        comparisons = 0

        for i in range(1, len(tasks)):
            key_task = tasks[i]
            key_weight = priority_weights.get(key_task.get("priority", "low"), 1)
            j = i - 1

            while j >= 0:
                comparisons += 1
                if priority_weights.get(tasks[j].get("priority", "low"), 1) < key_weight:
                    tasks[j + 1] = tasks[j]
                    j -= 1
                else:
                    break

            tasks[j + 1] = key_task

        return tasks, comparisons

    # ---------- 2. LINEAR SEARCH (title mein substring match, case-insensitive) ----------
    @staticmethod
    def linear_search(tasks: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        query = query.lower()
        matched = []
        for task in tasks:
            if query in task.get("title", "").lower():
                matched.append(task)
        return matched

    # ---------- 2b. COUNTING VERSION ----------
    @staticmethod
    def linear_search_counted(tasks: List[Dict[str, Any]], query: str) -> Tuple[List[Dict[str, Any]], int]:
        query = query.lower()
        matched = []
        comparisons = 0
        for task in tasks:
            comparisons += 1
            if query in task.get("title", "").lower():
                matched.append(task)
        return matched, comparisons

    # ---------- 3. BINARY SEARCH (sorted list mein exact/prefix title match) ----------
    @staticmethod
    def binary_search(sorted_tasks: List[Dict[str, Any]], target_title: str) -> Dict[str, Any] | None:
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

    # ---------- 3b. COUNTING VERSION ----------
    @staticmethod
    def binary_search_counted(sorted_tasks: List[Dict[str, Any]], target_title: str) -> Tuple[Dict[str, Any] | None, int]:
        target_title = target_title.lower()
        low, high = 0, len(sorted_tasks) - 1
        comparisons = 0

        while low <= high:
            comparisons += 1
            mid = (low + high) // 2
            mid_title = sorted_tasks[mid].get("title", "").lower()

            if mid_title == target_title:
                return sorted_tasks[mid], comparisons
            elif mid_title < target_title:
                low = mid + 1
            else:
                high = mid - 1

        return None, comparisons