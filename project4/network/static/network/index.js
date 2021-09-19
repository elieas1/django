function edit(elem){

    const span = elem.parentNode.parentNode.parentNode.getElementsByClassName("content")[0].querySelector("span")
    const content = elem.parentNode.parentNode.parentNode.getElementsByClassName("content")[0]
    elem.style.display = "none"
    span.style.display = "none"

    //textarea
    const textarea = document.createElement('textarea');
    textarea.style.cssText = "width:1000px"

    //div
    const div = document.createElement('div');
    div.style.cssText = "display:flex;flex-direction:row;margin-top:10px"

    //save button
    const save = document.createElement('button');
    save.innerHTML = "Save"
    save.style.cssText = "color: white;background-color:rgb(0, 0, 30);width:150px"

    //cancel button
    const cancel = document.createElement('button');
    cancel.innerHTML = "Cancel"
    cancel.style.cssText = "color: rgb(0, 0, 30);background-color:white;width:150px;margin-left:10px"
    
    //append buttons
    content.append(textarea)
    content.append(div)
    div.append(save)
    div.append(cancel)

    elem.parentNode.style.cssText = "display:flex;flex-direction:column"
    const id = elem.parentNode.getElementsByClassName("postid")[0].value

    fetch(`http://127.0.0.1:8000/post/${id}`)
    .then(response => {
        if(!response.ok){
            throw 'Error'
        }
        return response.json()
    })
    .then(post =>{
        console.log(post);
        textarea.value = post.post
    })

    // cancel button action
    cancel.addEventListener("click" , function(){
        elem.style.display = "block"
        textarea.style.display = "none"
        cancel.style.display = "none"
        save.style.display = "none"
        div.style.display = "none"
        span.style.display = "block"
    })

    // save button action
    save.addEventListener("click" , function(){
        fetch(`http://127.0.0.1:8000/post/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                posts: textarea.value         
            })
          })
        console.log(textarea.value)
        span.innerText = textarea.value
        span.style.display = "block"
        textarea.style.display = "none";
        elem.style.display = "block"
        save.style.display = "none"
        cancel.style.display = "none"
        div.style.display = "none"
        setTimeout(() => {
            alert("Post Edited Successfully")
        }, 100);
    })


}

function like(elem){
    const id = elem.parentNode.getElementsByClassName("postid")[0].value
    elem.disabled = true

    if(elem.style.color == "white"){
        fetch(`http://127.0.0.1:8000/post/${id}`)
        .then(response => {
            if(!response.ok){
                throw 'Error'
            }
            return response.json()
        })
        .then(post =>{
            console.log(post);
            fetch(`http://127.0.0.1:8000/post/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    
                    likes: post.likes-1   
                })
              })
            elem.parentNode.parentNode.parentNode.getElementsByClassName("likes")[0].innerText = `likes : ${post.likes-1}`
            elem.style.cssText = "color:rgb(0, 0, 30);background-color: white"
        })
    }
    else{
        fetch(`http://127.0.0.1:8000/post/${id}`)
        .then(response => {
            if(!response.ok){
                throw 'Error'
            }
            return response.json()
        })
        .then(post =>{
            console.log(post);
            fetch(`http://127.0.0.1:8000/post/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    
                    likes: post.likes + 1  
                })
              })
            elem.parentNode.parentNode.parentNode.getElementsByClassName("likes")[0].innerText = `likes : ${post.likes+1}`
            elem.style.cssText = "color:white;background-color: rgb(0, 0, 30)"
        })
    }


    fetch(`http://127.0.0.1:8000/post/${id}`,{
        method: 'POST',
        body: JSON.stringify({
            like: id
        })
      })
      setTimeout(() =>{elem.disabled = false},500)
}

document.getElementById("form").onsubmit = function(){
    alert("Form Submitted Successfully")
}