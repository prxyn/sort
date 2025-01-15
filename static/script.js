const canvas = document.getElementById("visualiser");
const ctx = canvas.getContext("2d");
let array = [];
let interval;

const complexities = {
  quick_sort: {
    time: (n) => `${n} log ${n} ≈ ${Math.round(n * Math.log2(n))}`,
    space: "O(log n)",
    desc: "Quick Sort is fast but not stable.",
  },
  merge_sort: {
    time: (n) => `${n} log ${n} ≈ ${Math.round(n * Math.log2(n))}`,
    space: "O(n)",
    desc: "Merge Sort uses extra memory for merging.",
  },
  bubble_sort: {
    time: (n) => `${n}² ≈ ${n * n}`,
    space: "O(1)",
    desc: "Bubble Sort is slow but simple.",
  },
  selection_sort: {
    time: (n) => `${n}² ≈ ${n * n}`,
    space: "O(1)",
    desc: "Selection Sort always compares every element.",
  },
  heap_sort: {
    time: (n) => `${n} log ${n} ≈ ${Math.round(n * Math.log2(n))}`,
    space: "O(1)",
    desc: "Heap Sort is efficient but not stable.",
  },
  insertion_sort: {
    time: (n) => (n === 1 ? "O(1)" : `${n}² ≈ ${n * n}`),
    space: "O(1)",
    desc: "Insertion Sort is good for nearly sorted arrays.",
  },
  shell_sort: {
    time: (n) => `${n}^(3/2) ≈ ${Math.round(n ** 1.5)}`,
    space: "O(1)",
    desc: "Shell Sort improves Insertion Sort using gaps.",
  },
  comb_sort: {
    time: (n) => `${n} log ${n} ≈ ${Math.round(n * Math.log2(n))}`,
    space: "O(1)",
    desc: "Comb Sort improves Bubble Sort with gaps.",
  },
  random_quick_sort: {
    time: (n) => `${n} log ${n} ≈ ${Math.round(n * Math.log2(n))}`,
    space: "O(log n)",
    desc: "Randomised Quick Sort reduces the chances of worst-case time complexity by choosing a random pivot.",
  },
};


function drawArray(arr) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const barWidth = canvas.width / arr.length;
  for (let i = 0; i < arr.length; i++) {
    const barHeight = arr[i] * (canvas.height / Math.max(...arr)) - 2;
    ctx.fillStyle = "blue";
    ctx.fillRect(
      i * barWidth,
      canvas.height - barHeight,
      barWidth - 2,
      barHeight
    );
  }
}


function generateArray() {
  array = Array.from({ length: 30 }, () => Math.floor(Math.random() * 100) + 1);
  document.getElementById("arrayInput").value = array.join(",");
  drawArray(array);
  updateComplexity();
}


async function startSort() {
  clearInterval(interval);

  const algorithm = document.getElementById("algorithm").value;
  const order = document.getElementById("order").value;
  const inputArray = document.getElementById("arrayInput").value;
  array = inputArray ? inputArray.split(",").map(Number) : array;

  const response = await fetch("/sort", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ algorithm, array, order }),
  });

  if (response.ok) {
    const steps = await response.json();
    animateSteps(steps);
  } else {
    console.error("Error fetching sorting steps:", response.statusText);
  }
}


function animateSteps(steps) {
  let i = 0;
  clearInterval(interval);
  interval = setInterval(() => {
    if (i >= steps.length) {
      clearInterval(interval);
      return;
    }
    drawArray(steps[i]);
    i++;
  }, 50);
}


function updateComplexity() {
  const algorithm = document.getElementById("algorithm").value;
  const arraySize = array.length;

  if (arraySize === 0) {
    console.error("Array is empty. Cannot calculate complexities.");
    document.getElementById("timeComplexity").innerText = "Array is empty.";
    document.getElementById("spaceComplexity").innerText = "-";
    document.getElementById("algorithmDescription").innerText = "-";
    return;
  }

  if (complexities[algorithm]) {
    const { time, space, desc } = complexities[algorithm];
    document.getElementById("timeComplexity").innerText = time(arraySize);
    document.getElementById("spaceComplexity").innerText = space;
    document.getElementById("algorithmDescription").innerText = desc;
  } else {
    document.getElementById("timeComplexity").innerText = "-";
    document.getElementById("spaceComplexity").innerText = "-";
    document.getElementById("algorithmDescription").innerText = "-";
  }
}


function handleAlgorithmChange() {
  const algorithm = document.getElementById("algorithm").value;
  const options = document.querySelectorAll("#algorithm option");
  options.forEach((option) => {
    option.style.backgroundColor =
      option.value === algorithm ? "#e0f7fa" : "white";
  });

  updateComplexity();
}


document
  .getElementById("algorithm")
  .addEventListener("change", updateComplexity);
document.getElementById("arrayInput").addEventListener("input", () => {
  const inputArray = document.getElementById("arrayInput").value;
  array = inputArray.split(",").map(Number);
  updateComplexity();
});


generateArray();
