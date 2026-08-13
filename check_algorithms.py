import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.algorithms import AlgorithmsEngine

PASS = "PASS"
FAIL = "FAIL"

results = []


def check(test_name, actual, expected):
    status = PASS if actual == expected else FAIL
    results.append((test_name, status, actual, expected))
    print(f"[{status}] {test_name}")
    if status == FAIL:
        print(f"       expected: {expected}")
        print(f"       actual:   {actual}")


def make_task(title, priority="low"):
    return {"title": title, "priority": priority}


def run_tests():
    print("=" * 50)
    print("Testing insertion_sort_tasks (priority: high > medium > low)")
    print("=" * 50)

    tasks = [
        make_task("Task A", "low"),
        make_task("Task B", "high"),
        make_task("Task C", "medium"),
        make_task("Task D", "high"),
        make_task("Task E", "low"),
    ]
    sorted_tasks = AlgorithmsEngine.insertion_sort_tasks(tasks)
    sorted_priorities = [t["priority"] for t in sorted_tasks]

    check(
        "insertion_sort_tasks - high priority tasks come first",
        sorted_priorities[:2] == ["high", "high"] or set(sorted_priorities[:2]) == {"high"},
        True,
    )

    check(
        "insertion_sort_tasks - low priority tasks come last",
        sorted_priorities[-2:] == ["low", "low"] or set(sorted_priorities[-2:]) == {"low"},
        True,
    )

    check(
        "insertion_sort_tasks - original list not mutated",
        tasks[0]["priority"],
        "low",
    )

    check(
        "insertion_sort_tasks - empty list",
        AlgorithmsEngine.insertion_sort_tasks([]),
        [],
    )

    check(
        "insertion_sort_tasks - single element",
        AlgorithmsEngine.insertion_sort_tasks([make_task("Solo", "medium")]),
        [make_task("Solo", "medium")],
    )

    print()
    print("=" * 50)
    print("Testing linear_search (substring match in title, case-insensitive)")
    print("=" * 50)

    tasks2 = [
        make_task("Submit report"),
        make_task("Fix login bug"),
        make_task("Design Homepage"),
        make_task("Write unit tests"),
    ]

    check(
        "linear_search - exact case match",
        AlgorithmsEngine.linear_search(tasks2, "login"),
        [make_task("Fix login bug")],
    )

    check(
        "linear_search - case-insensitive match",
        AlgorithmsEngine.linear_search(tasks2, "HOMEPAGE"),
        [make_task("Design Homepage")],
    )

    check(
        "linear_search - no match",
        AlgorithmsEngine.linear_search(tasks2, "xyz"),
        [],
    )

    check(
        "linear_search - empty list",
        AlgorithmsEngine.linear_search([], "report"),
        [],
    )

    print()
    print("=" * 50)
    print("Testing binary_search (list must be pre-sorted by title)")
    print("=" * 50)

    sorted_by_title = sorted(
        [
            make_task("Apple task"),
            make_task("Banana task"),
            make_task("Cherry task"),
            make_task("Date task"),
        ],
        key=lambda t: t["title"].lower(),
    )

    check(
        "binary_search - element present",
        AlgorithmsEngine.binary_search(sorted_by_title, "Cherry task"),
        make_task("Cherry task"),
    )

    check(
        "binary_search - element present (case-insensitive)",
        AlgorithmsEngine.binary_search(sorted_by_title, "apple task"),
        make_task("Apple task"),
    )

    check(
        "binary_search - element not present",
        AlgorithmsEngine.binary_search(sorted_by_title, "Mango task"),
        None,
    )

    check(
        "binary_search - empty list",
        AlgorithmsEngine.binary_search([], "Apple task"),
        None,
    )


def print_summary():
    print()
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    total = len(results)
    passed = sum(1 for r in results if r[1] == PASS)
    failed = total - passed
    print(f"Total tests: {total}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")
    if failed == 0:
        print("\nAll tests passed! ✅")
    else:
        print("\nSome tests failed. ❌")
        for name, status, actual, expected in results:
            if status == FAIL:
                print(f"  - {name}: expected {expected}, got {actual}")


if __name__ == "__main__":
    run_tests()
    print_summary()
