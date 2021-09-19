document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("messagebutton")
    .addEventListener("click", () => openmessages());
  document
    .getElementById("inbox")
    .addEventListener("click", () => loadmailbox("inbox"));
  document
    .getElementById("sent")
    .addEventListener("click", () => loadmailbox("sent"));
  document
    .getElementById("archived")
    .addEventListener("click", () => loadmailbox("archived"));
  document
    .getElementById("compose")
    .addEventListener("click", () => loadmailbox("compose"));
  document.getElementById("compose-recipients").onkeyup = function () {
    like();
  };
  document.getElementById("compose-form").onsubmit = function () {
    sendmail();
    return false;
  };
});

function loadmailbox(type) {
  document.getElementById(`emails-view`).innerText = "";
  document.getElementById(`sent`).style.backgroundColor = " rgb(50, 50, 250)";
  document.getElementById(`inbox`).style.backgroundColor = " rgb(50, 50, 250)";
  document.getElementById(`archived`).style.backgroundColor =
    " rgb(50, 50, 250)";
  document.getElementById(`compose`).style.backgroundColor =
    " rgb(50, 50, 250)";
  document.getElementById(`compose-view`).style.display = "none";
  document.getElementById(`emails-view`).style.display = "none";
  document.getElementById(`${type}`).style.backgroundColor = "red";
  if (type !== "compose") {
    document.getElementById(`emails-view`).style.display = "";
    fetch(`http://127.0.0.1:8000/api/${type}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        data.mail.forEach((email) => {
          emailbox = document.createElement("div");
          emailbox.id = "emailbox";
          document.getElementById("emails-view").append(emailbox);
          sender = document.createElement("div");
          emailbox.append(sender);
          if (type !== "sent") {
            sender.innerText = email.sender;
          } else if (type == "sent") {
            sender.innerText = email.recipient;
          }
          sender.style.cssText = "font-weight:bold";
          subject = document.createElement("div");
          subject.id = "subject";
          emailbox.append(subject);
          subject.innerText = email.subject;
          timestamp = document.createElement("div");
          emailbox.append(timestamp);
          timestamp.innerText = email.timestamp;
        });
      });
  } else if (type == "compose") {
    document.getElementById(`emails-view`).style.display = "none";
    document.getElementById(`compose-view`).style.display = "block";
  }
}

function openmessages() {
  document.getElementById("messages").style.display = "block";
  loadmailbox("inbox");
}
function closemessages() {
  document.getElementById("messages").style.display = "none";
}

function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function (event) {
  if (!event.target.matches(".dropbtn")) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains("show")) {
        openDropdown.classList.remove("show");
      }
    }
  }
};

function openform() {
  document.getElementById("form").style.display = "block";
}

function closeform() {
  document.getElementById("form").style.display = "none";
}

function like() {
  value = document.getElementById("compose-recipients").value;
  help = document.getElementById("recipient-help");
  if (value !== "") {
    fetch(`http://127.0.0.1:8000/api1/${value}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        data.user.forEach((name) => {
          help.innerText = "";
          help.append(name);
        });
      });
  } else {
    help.innerText = "";
  }
}

function sendmail() {
  const csrftoken = getCookie("csrftoken");
  const request = new Request(`http://127.0.0.1:8000/api/compose`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  fetch(request, {
    method: "POST",
    mode: "same-origin",
    body: JSON.stringify({
      recipients: document.getElementById("compose-recipients").value,
      subject: document.getElementById("compose-subject").value,
      body: document.getElementById("compose-body").value,
    }),
  });
  setTimeout(() => {
    loadmailbox("sent");
  }, 200);

  return false;
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
