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
  input.className = "user";
  input.placeholder = "User email";
  input.setAttribute("required", "");
  input.focus();

  const deleteButton = document.createElement("button");
  deleteButton.type = "button";
  deleteButton.innerHTML = "×";
  deleteButton.className = "remove";
  deleteButton.onclick = () => removeUserInput(inputContainer);
  inputContainer.appendChild(deleteButton);
}

function newImage() {
  let container = document.getElementById("img-container");
  let selectedImg = document.getElementsByClassName("selected-img");
  let file = document.getElementById("picture");
  let fileName = file.value.split("\\").pop();

  if (selectedImg.length > 0) {
    let f = selectedImg[0];
    if (fileName != "") {
      f.innerHTML = fileName + "<img class='check' src='/static/img/check-solid.svg'>";
    } else {
      container.removeChild(f);
    }
    
  } else if (fileName != "") {
    let f = document.createElement("p");
    f.className = "selected-img";
    f.innerHTML = fileName + "<img class='check' src='/static/img/check-solid.svg'>";
    container.appendChild(f);
  }
}
