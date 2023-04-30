// Functions
function addSubtask(task) {
  // Form
  addTaskForm.querySelector("form").action = "/tasks/add/";
  addTaskForm.querySelector("h2").innerHTML = "Add Subtask";
  addTaskForm.querySelector("input[name='name']").value = "";
  addTaskForm.querySelector("textarea[name='description']").innerHTML = "";
  addTaskForm.querySelector("input[name='start']").value = "";
  addTaskForm.querySelector("input[name='end']").value = "";
  addTaskForm.querySelector("*[name='color']").value = "";
  // Hide details
  details.innerHTML = "";
  // Set parent task
  parentTaskInput.value = task.dataset.id;
  subtaskLabel.innerHTML = "Subtask of: <b>" + task.dataset.name + "</b>";
  // Show form
  addTaskForm.style.display = "block";
}

function editTask(task) {
  // Form
  addTaskForm.querySelector("form").action =
    "/tasks/edit/" + task.dataset.id + "/";
  addTaskForm.querySelector("h2").innerHTML = "Edit Task";
  addTaskForm.querySelector("input[name='name']").value = task.dataset.name;
  addTaskForm.querySelector("textarea[name='description']").innerHTML =
    task.dataset.description;
  addTaskForm.querySelector("input[name='start']").value = task.dataset.start;
  addTaskForm.querySelector("input[name='end']").value = task.dataset.end;
  addTaskForm.querySelector("*[name='color']").value = task.dataset.color;
  // Hide details
  details.innerHTML = "";
  // Set parent task
  parentTaskInput.value = task.dataset.id;
  subtaskLabel.innerHTML = "";
  // Show form
  addTaskForm.style.display = "block";
}

function deleteTask(task) {
  location.assign("/tasks/delete/" + task.dataset.id + "/");
}

// Task Focus
let focusedTask;
let focusedParentTask;
function focusTask(taskElement) {
  // Remove highlight from previous task if any
  if (focusedTask) focusedTask.classList.remove("focused");
  if (focusedParentTask) focusedParentTask.classList.remove("subtask-focused");
  // Highlight
  taskElement.classList.add("focused");
  focusedTask = taskElement;
  // Highlight parent
  if (taskElement.dataset.parent != "None") {
    const parent = tasks.querySelector(
      "#tasks > .task[data-id='" + taskElement.dataset.parent + "']"
    );
    parent.classList.add("subtask-focused");
    focusedParentTask = parent;
  } else {
    taskElement.classList.add("subtask-focused");
    focusedParentTask = taskElement;
  }

  // Display details
  details.innerHTML = `
    <h2 class='task-title'>${taskElement.dataset.name}</h2>
    <div style='text-align: center;'>
      <button class='tool' title="Add subtask"><i class="fa-solid fa-plus"></i></button>
      <button class='tool' title="Edit"><i class="fa-solid fa-pencil"></i></button>
      <button class='tool' title="Delete"><i class="fa-solid fa-trash"></i></button>
    </div>
    <p class="description">${taskElement.dataset.description}</p>
    <p class="description">Start Date: ${taskElement.dataset.start}</p>
    <p class="description">End Date: ${taskElement.dataset.end}</p>
  `;
  details.querySelector("button[title='Add subtask']").onclick = () => {
    addSubtask(taskElement);
  };
  details.querySelector("button[title='Edit']").onclick = () => {
    editTask(taskElement);
  };
  details.querySelector("button[title='Delete']").onclick = () => {
    deleteTask(taskElement);
  };

  // Hide form
  addTaskForm.style.display = "none";
}

// Tasks
const DAY_LENGTH = 60;
const DAY = 24 * 60 * 60 * 1000;
let firstDate;
let lastDate;
for (let taskElement of tasks.querySelectorAll(".task")) {
  if (!firstDate) firstDate = new Date(taskElement.dataset.start);
  lastDate = new Date(taskElement.dataset.end);

  // Event Listener
  taskElement.children[0].onclick = (event) => {
    let task = document.getElementById("t");
    if (task.classList.contains("hide")) {
      showSidebanner();
    }
    event.stopPropagation();
    focusTask(taskElement);
  };
  // Styling
  let durate =
    new Date(taskElement.dataset.end) -
    new Date(taskElement.dataset.start) +
    1 * DAY;
  let offset = new Date(taskElement.dataset.start) - firstDate;
  taskElement.style.setProperty("--width", (durate / DAY) * DAY_LENGTH + "px");
  taskElement.style.setProperty("--left", (offset / DAY) * DAY_LENGTH + "px");
}

// Week labels
const WEEK_LENGTH = 7 * DAY_LENGTH;
const WEEK = 7 * DAY;
let weekStart = firstDate;
while (weekStart.getTime() < lastDate.getTime()) {
  const week = document.createElement("div");
  weeks.appendChild(week);
  week.classList.add("week");
  week.innerHTML = weekStart.toLocaleDateString("en-CA", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });

  weekStart = new Date(weekStart.getTime() + 1 * WEEK);
}
weeks.style.setProperty("--width", WEEK_LENGTH + "px");

// Unfocus
overview.onclick = () => {
  hideSidebanner();
};

/*************************************************************************************
 * Banner functions
 */
const taskBanner = document.getElementById("t");

function hideSidebanner() {
  taskBanner.classList.add("hide");
}

function showSidebanner() {
  taskBanner.classList.remove("hide");
}

function returnToAddTask() {
  details.innerHTML = "";

  if (focusedTask) focusedTask.classList.remove("focused");
  focusedTask = null;
  if (focusedParentTask) focusedParentTask.classList.remove("subtask-focused");
  focusedParentTask = null;
  parentTaskInput.removeAttribute("value");

  // Show form
  addTaskForm.style.display = "block";
}

function addTaskBanner() {
  details.innerHTML = "";

  if (focusedTask) focusedTask.classList.remove("focused");
  focusedTask = null;
  if (focusedParentTask) focusedParentTask.classList.remove("subtask-focused");
  focusedParentTask = null;
  parentTaskInput.removeAttribute("value");

  addTaskForm.querySelector("form").action = "/tasks/add/";
  addTaskForm.querySelector("h2").innerHTML = "Add Task";
  addTaskForm.querySelector("input[name='name']").value = "";
  addTaskForm.querySelector("textarea[name='description']").innerHTML = "";
  addTaskForm.querySelector("input[name='start']").value = "";
  addTaskForm.querySelector("input[name='end']").value = "";
  addTaskForm.querySelector("*[name='color']").value = "";

  subtaskLabel.innerHTML = "";

  addTaskForm.style.display = "block";
  showSidebanner();
}
