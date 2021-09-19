document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("navwrapper").style.cssText =
    "border-bottom:1px solid lightgrey";
  document
    .querySelector("#loadposts")
    .addEventListener("click", () => loadposts("posts"));
  document
    .querySelector("#loadfollowers")
    .addEventListener("click", () => loadposts("followers"));
  document
    .querySelector("#loadfollowing")
    .addEventListener("click", () => loadposts("following"));
  document
    .querySelector("#loadcomments")
    .addEventListener("click", () => loadposts("comments"));
  document
    .querySelector("#sendmessage")
    .addEventListener("click", () => openmessages());
});

function loadposts(type) {
  document.querySelector("#loadposts").style.cssText =
    "border-bottom:2px solid white;transition:400ms";
  document.querySelector("#loadcomments").style.cssText =
    "border-bottom:2px solid white;transition:400ms";
  document.querySelector("#loadfollowing").style.cssText =
    "border-bottom:2px solid white;transition:400ms";
  document.querySelector("#loadfollowers").style.cssText =
    "border-bottom:2px solid white;transition:400ms";
  document.querySelector(`#load${type}`).style.cssText =
    "border-bottom:2px solid red;transition:400ms";

  document.querySelector("#info").innerText = "";

  user = document.getElementById("username").innerText;
  fetch(`/api/${type}/${user}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data == "") {
        empty = document.createElement("div");
        if (type == "comments") {
          empty.innerText = "No Comments";
        } else if (type == "posts") {
          empty.innerText = "No Posts";
        }
        document.querySelector("#info").append(empty);
      }
      data.query.forEach((element) => {
        if (type == "posts") {
          eachpost = document.createElement("div");
          eachpost.id = "eachpost";
          document.querySelector("#info").append(eachpost);
          date = document.createElement("div");
          date.innerText = element.date;
          document.querySelector("#eachpost").append(date);
          title = document.createElement("div");
          title.id = "title";
          document.querySelector("#eachpost").append(title);
          title.innerText = element.title;
          body = document.createElement("div");
          body.innerText = element.body;
          document.querySelector("#eachpost").append(body);
          likes = document.createElement("div");
          likes.innerText = element.likes;
          document.querySelector("#eachpost").append(likes);
          hr = document.createElement("hr");
          document.querySelector("#eachpost").append(hr);
        } else if (type == "comments") {
          eachcomment = document.createElement("div");
          eachcomment.id = "eachcomment";
          document.querySelector("#info").append(eachcomment);
          date = document.createElement("div");
          date.innerText = element.date;
          document.querySelector("#eachcomment").append(date);
          posttitle = document.createElement("div");
          posttitle.innerText = element.post;
          document.querySelector("#eachcomment").append(posttitle);
          comment = document.createElement("div");
          comment.innerText = element.comment;
          document.querySelector("#eachcomment").append(comment);
        } else if (type == "followers") {
          i = -1;
          followers = document.createElement("div");
          followers.id = "followers";
          document.querySelector("#info").append(followers);
          followercount = document.createElement("div");
          followercount.id = "followercount";
          followercount.innerText = `${element.followercount} followers`;
          followers.append(followercount);
          element.followers.forEach((name) => {
            i++;
            nameoffollowers = document.createElement("div");
            nameoffollowers.id = "nameoffollowers";
            followers.append(nameoffollowers);
            username = document.createElement("div");
            namelink = document.createElement("a");
            namelink.href = `${name}`;
            namelink.innerText = name;
            namelink.className = "userlink";
            username.append(namelink);
            nameoffollowers.append(username);

            followbutton = document.createElement("button");
            followbutton.id = "followbutton";
            if (data.user[0].username == name) {
            } else {
              nameoffollowers.append(followbutton);
            }
            insidebuttontext = document.createElement("div");
            if (data.user[0].following.includes(name)) {
              insidebuttontext.innerText = "UnFollow";
            } else {
              insidebuttontext.innerText = "Follow";
            }
            followbutton.append(insidebuttontext);

            followbutton.onclick = function (event) {
              const csrftoken = getCookie("csrftoken");
              const request = new Request(
                `http://127.0.0.1:8000/profile/${name}`,
                { headers: { "X-CSRFToken": csrftoken } }
              );

              if (event.target.innerText == "Follow") {
                event.target.innerText = "UnFollow";
              } else {
                event.target.innerText = "Follow";
              }
              fetch(request, {
                method: "PUT",
                mode: "same-origin",
                body: JSON.stringify({
                  user: user,
                }),
              });
              fetch(`/api/${type}/${user}`)
                .then((response) => response.json())
                .then((data) => {
                  document.getElementById(
                    "loadfollowing"
                  ).innerHTML = `${data.user[0].followingcount} Following`;
                });
            };
          });
        } else if (type == "following") {
          i = -1;
          following = document.createElement("div");
          following.id = "following";
          document.querySelector("#info").append(following);
          followingcount = document.createElement("div");
          followingcount.id = "followingcount";
          followingcount.innerText = `${element.followingcount} following`;
          following.append(followingcount);
          element.following.forEach((name) => {
            i++;
            nameoffollowing = document.createElement("div");
            nameoffollowing.id = "nameoffollowing";
            following.append(nameoffollowing);
            username = document.createElement("div");
            namelink = document.createElement("a");
            namelink.href = `${name}`;
            namelink.innerText = name;
            namelink.className = "userlink";
            username.append(namelink);
            nameoffollowing.append(username);

            followbutton = document.createElement("button");
            followbutton.id = "followbutton";
            if (data.user[0].username === name) {
            } else {
              nameoffollowing.append(followbutton);
            }
            insidebuttontext = document.createElement("div");

            if (data.user[0].following.includes(name)) {
              insidebuttontext.innerText = "UnFollow";
            } else {
              insidebuttontext.innerText = "Follow";
            }
            followbutton.append(insidebuttontext);

            followbutton.onclick = function (event) {
              const csrftoken = getCookie("csrftoken");
              const request = new Request(
                `http://127.0.0.1:8000/profile/${name}`,
                { headers: { "X-CSRFToken": csrftoken } }
              );

              if (event.target.innerText == "Follow") {
                event.target.innerText = "UnFollow";
              } else {
                event.target.innerText = "Follow";
              }
              fetch(request, {
                method: "PUT",
                mode: "same-origin",
                body: JSON.stringify({
                  user: user,
                }),
              });
              fetch(`/api/${type}/${user}`)
                .then((response) => response.json())
                .then((data) => {
                  document.getElementById(
                    "loadfollowing"
                  ).innerHTML = `${data.user[0].followingcount} Following`;
                });
            };
          });
        }
      });
    });
}

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
    username = document.getElementById("username").innerText;
    document.getElementById(`emails-view`).style.display = "none";
    document.getElementById(`compose-view`).style.display = "block";
    document.getElementById("compose-recipients").value = username;
  }
}


function openmessages() {
  document.getElementById("messages").style.display = "block";
  loadmailbox("compose");
}

function followprofile(elem) {
  user = document.getElementById("username").innerText;

  const csrftoken = getCookie("csrftoken");
  const request = new Request(`http://127.0.0.1:8000/profile/${user}`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  if (elem.innerText == "Follow") {
    elem.innerText = "UnFollow";
  } else {
    elem.innerText = "Follow";
  }
  fetch(request, {
    method: "PUT",
    mode: "same-origin",
    body: JSON.stringify({
      user: user,
    }),
  });
  setTimeout(function () {
    fetch(`/api/following/${user}`)
      .then((response) => response.json())
      .then((data) => {
        document.getElementById(
          "loadfollowers"
        ).innerHTML = `${data.query[0].followercount} Followers`;
      });
  }, 200);
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

function opendescription() {
  document.getElementById("description").style.display = "block";
}

function closedescription() {
  document.getElementById("description").style.display = "none";
}
