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