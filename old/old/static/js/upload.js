const uploadForm = document.getElementById("submitCV");
const uploadError = document.getElementById("upload-error");
const uploadResult = document.getElementById("upload-result");
const fileInput = document.getElementById("file");
uploadForm.onsubmit = (event) => {
  event.preventDefault();
  try {
    const files = event.target.file.files;
    const file = files[0];
    const fileName = event.target.file.files[0].name;
    const fileSize = event.target.file.files[0].size;
    const ext = fileName.split(".").pop();
    if (files.length > 1) {
      uploadError.innerText = "Please choose only 1 file";
      return;
    } else if (fileSize > 1000000) {
      uploadError.innerText = "Please upload a file not bigger than 1 mb";
      return;
    } else if (ext !== "pdf" && ext !== "docx") {
      uploadError.innerText = "Only pdf and word files are allowed";
      return;
    } else {
      let data = new FormData();
      data.append("file", file);
      data.append(
        "csrfmiddlewaretoken",
        document.getElementsByName("csrfmiddlewaretoken")[0].value
      );
      fetch("http://127.0.0.1:8000/api/upload", {
        method: "POST",
        body: data,
        credentials: "same-origin",
      }).then((response) => {
        if (response.ok) {
          uploadResult.innerText = "Upload Successful";
        } else {
          error = new Error("Something Went Wrong, please try again!");
          uploadResult.innerText = error.message;
          throw error;
        }
      });
    }
  } catch (e) {
    uploadError.innerText = "Please upload a file";
    return;
  }
};

fileInput.onchange = () => {
  uploadError.innerText = "";
  uploadResult.innerText = "";
};
