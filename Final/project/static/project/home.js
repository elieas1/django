function string_to_slug(str) {
  str = str.replace(/^\s+|\s+$/g, ""); // trim
  str = str.toLowerCase();

  var from = "àáãäâèéëêìíïîòóöôùúüûñç·/_,:;";
  var to = "aaaaaeeeeiiiioooouuuunc------";

  for (var i = 0, l = from.length; i < l; i++) {
    str = str.replace(new RegExp(from.charAt(i), "g"), to.charAt(i));
  }

  str = str
    .replace(/[^a-z0-9 -]/g, "") // remove invalid chars
    .replace(/\s+/g, "-") // collapse whitespace and replace by -
    .replace(/-+/g, "-"); // collapse dashes

  return str;
}

function opencomments(elem) {
  const hidden = elem.parentNode.parentNode.parentNode.parentNode.childNodes[3];
  state(hidden, elem);
}

function state(text, elem) {
  number = elem;
  username =
    elem.parentNode.parentElement.parentElement.childNodes[1].childNodes[3]
      .childNodes[0].innerText;
  post = string_to_slug(
    elem.parentNode.parentElement.parentElement.childNodes[3].childNodes[0]
      .innerText
  );
  show =
    elem.parentElement.parentElement.parentElement.parentElement.childNodes[3]
      .childNodes[1].childNodes[3];
  if (text.hidden == true) {
    text.hidden = false;
    showcommentsdiv(username, post, show);
  } else {
    text.hidden = true;
  }
}

function showcommentsdiv(username, post, show) {
  show.innerText = "";
  fetch(`api/comment/${post}/${username}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.length !== 0) {
        data.forEach((com) => {
          eachcomment = document.createElement("div");
          eachcomment.id = "eachcomment";
          imageanduser = document.createElement("div");
          imageanduser.id = "imageandusercomment";
          eachcomment.append(imageanduser);
          show.append(eachcomment);

          image = document.createElement("img");
          image.src = com.user.image;
          image.style.cssText = "border-radius:25px";
          image.width = 40;
          imageanduser.append(image);

          commentor = document.createElement("a");
          commentor.href = `/profile/${com.user.username}`;
          commentor.innerText = com.user.username;
          commentor.style.cssText = "margin-left:5px";
          imageanduser.append(commentor);

          comment = document.createElement("div");
          comment.innerText = com.comment;
          comment.style.cssText = "margin-left:45px;margin-top:10px";
          eachcomment.append(comment);

          date = document.createElement("div");
          date.innerText = com.date;
          date.style.cssText = "margin-left:10px;font-size:10px";
          imageanduser.append(date);

          if (data.length == 1) {
            number.innerText = `1 Comment`;
          } else {
            number.innerText = `${data.length} Comments`;
          }
        });
      }
    });
}

function addcomment(event) {
  title =
    event.parentElement.parentElement.parentElement.parentElement.childNodes[1]
      .childNodes[3].childNodes[0].childNodes[0].innerText;

  input = document.querySelector(".addcommentinput");
  const csrftoken = getCookie("csrftoken");
  const request = new Request(`http://127.0.0.1:8000/api/comment/user/post`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  fetch(request, {
    method: "POST",
    mode: "same-origin",
    body: JSON.stringify({
      comment: input.value,
      post: title,
    }),
  });
  input.value = "";
  setTimeout(() => {
    showcommentsdiv(username, post, show);
  }, 300);
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

async function upvote(event) {
  console.log(location.host);
  title = string_to_slug(
    event.parentElement.parentElement.parentElement.childNodes[3].childNodes[0]
      .innerText
  );
  unslugtitle =
    event.parentElement.parentElement.parentElement.childNodes[3].childNodes[0]
      .innerText;
  user =
    event.parentElement.parentElement.parentElement.childNodes[1].childNodes[3]
      .childNodes[0].innerText;

  const csrftoken = getCookie("csrftoken");
  const request = new Request(`/api1/${title}`, {
    headers: { "X-CSRFToken": csrftoken },
  });

    await fetch(request, {
    method: "PUT",
    body: JSON.stringify({ post: title, user: user }),
  }); 

  fetch(`http://127.0.0.1:8000/api1/${title}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.array.includes(unslugtitle)) {
        event.style.border = "2px solid rgb(50,50,250)";
      } else {
        event.style.border = "2px solid rgb(231, 231, 231)";
      }
      event.innerText = data.likes;
    });
}
