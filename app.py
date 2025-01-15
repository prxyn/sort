from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def quick_sort_steps(arr, order):
    steps = []

    def quick_sort(arr, low, high):
        if low < high:
            pivot = partition(arr, low, high)
            quick_sort(arr, low, pivot - 1)
            quick_sort(arr, pivot + 1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if (order == "ascending" and arr[j] < pivot) or (
                order == "descending" and arr[j] > pivot
            ):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append(arr[:])
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append(arr[:])
        return i + 1

    quick_sort(arr, 0, len(arr) - 1)
    return steps


def merge_sort_steps(arr, order):
    steps = []

    def merge_sort(arr, start, end):
        if end - start > 1:
            mid = (start + end) // 2

            merge_sort(arr, start, mid)
            merge_sort(arr, mid, end)

            merge(arr, start, mid, end)

    def merge(arr, start, mid, end):
        left = arr[start:mid]
        right = arr[mid:end]

        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            if (order == "ascending" and left[i] <= right[j]) or (
                order == "descending" and left[i] >= right[j]
            ):
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            steps.append(arr[:])
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            steps.append(arr[:])

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            steps.append(arr[:])

    merge_sort(arr, 0, len(arr))
    return steps


def bubble_sort_steps(arr, order):
    steps = []
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if (order == "ascending" and arr[j] > arr[j + 1]) or (
                order == "descending" and arr[j] < arr[j + 1]
            ):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                steps.append(arr[:])
        if not swapped:
            break
    return steps


def selection_sort_steps(arr, order):
    steps = []
    n = len(arr)
    for i in range(n):
        min_or_max_idx = i
        for j in range(i + 1, n):
            if (order == "ascending" and arr[j] < arr[min_or_max_idx]) or (
                order == "descending" and arr[j] > arr[min_or_max_idx]
            ):
                min_or_max_idx = j
        if min_or_max_idx != i:
            arr[i], arr[min_or_max_idx] = arr[min_or_max_idx], arr[i]
            steps.append(arr[:])
    return steps


def heap_sort_steps(arr, order):
    steps = []

    def heapify(n, i):
        largest_or_smallest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and (
            (order == "ascending" and arr[left] > arr[largest_or_smallest])
            or (order == "descending" and arr[left] < arr[largest_or_smallest])
        ):
            largest_or_smallest = left
        if right < n and (
            (order == "ascending" and arr[right] > arr[largest_or_smallest])
            or (order == "descending" and arr[right] < arr[largest_or_smallest])
        ):
            largest_or_smallest = right
        if largest_or_smallest != i:
            arr[i], arr[largest_or_smallest] = arr[largest_or_smallest], arr[i]
            steps.append(arr[:])
            heapify(n, largest_or_smallest)

    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify(len(arr), i)

    for i in range(len(arr) - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        steps.append(arr[:])
        heapify(i, 0)

    return steps


def insertion_sort_steps(arr, order):
    steps = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and (
            (order == "ascending" and arr[j] > key)
            or (order == "descending" and arr[j] < key)
        ):
            arr[j + 1] = arr[j]
            j -= 1
            steps.append(arr[:])
        arr[j + 1] = key
        steps.append(arr[:])
    return steps


def shell_sort_steps(arr, order):
    steps = []
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and (
                (order == "ascending" and arr[j - gap] > temp)
                or (order == "descending" and arr[j - gap] < temp)
            ):
                arr[j] = arr[j - gap]
                steps.append(arr[:])
                j -= gap
            arr[j] = temp
            steps.append(arr[:])
        gap //= 2
    return steps


def comb_sort_steps(arr, order):
    steps = []
    gap = len(arr)
    shrink = 1.3
    sorted_ = False
    while not sorted_:
        gap = max(1, int(gap / shrink))
        sorted_ = True
        for i in range(len(arr) - gap):
            if (order == "ascending" and arr[i] > arr[i + gap]) or (
                order == "descending" and arr[i] < arr[i + gap]
            ):
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                steps.append(arr[:])
                sorted_ = False
    return steps


def random_quick_sort_steps(arr, order):
    import random

    steps = []

    def quick_sort(arr, low, high):
        if low < high:
            pivot_index = random.randint(low, high)
            arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

            pivot = partition(arr, low, high)

            quick_sort(arr, low, pivot - 1)
            quick_sort(arr, pivot + 1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if (order == "ascending" and arr[j] < pivot) or (
                order == "descending" and arr[j] > pivot
            ):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append(arr[:])
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append(arr[:])
        return i + 1

    quick_sort(arr, 0, len(arr) - 1)
    return steps


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sort", methods=["POST"])
def sort():
    data = request.json
    algorithm = data.get("algorithm")
    order = data.get("order", "ascending")
    arr = data.get("array")
    steps = []

    sorting_algorithms = {
        "quick_sort": quick_sort_steps,
        "merge_sort": merge_sort_steps,
        "bubble_sort": bubble_sort_steps,
        "selection_sort": selection_sort_steps,
        "heap_sort": heap_sort_steps,
        "insertion_sort": insertion_sort_steps,
        "shell_sort": shell_sort_steps,
        "comb_sort": comb_sort_steps,
        "random_quick_sort": random_quick_sort_steps,
    }

    sorting_function = sorting_algorithms.get(algorithm)

    if sorting_function:
        steps = sorting_function(arr, order)
    else:
        steps = []

    return jsonify(steps)


if __name__ == "__main__":
    app.run(debug=True)
