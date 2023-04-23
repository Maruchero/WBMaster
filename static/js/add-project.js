const users = document.getElementById("users");

function removeUserInput(inputContainer) {
  users.removeChild(inputContainer);
}

function addUserInput() {
  const inputContainer = document.createElement("div");
  users.appendChild(inputContainer);
  inputContainer.className = "user-input";

  const input = document.createElement("input");
  inputContainer.appendChild(input);
  input.name = "user";
  input.type = "email";
  input.class = "user";
  input.focus();

  const deleteButton = document.createElement("button");
  deleteButton.type = "button";
  deleteButton.innerHTML = "Remove";
  deleteButton.onclick = () => removeUserInput(inputContainer);
  inputContainer.appendChild(deleteButton);
}
