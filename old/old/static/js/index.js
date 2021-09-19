

var observer1 = new IntersectionObserver((entry)=>{
    entry.forEach(ent=>{
        if (ent.isIntersecting) {
            ent.target.src = "static/images/initiative.jpg";
            observer1.unobserve(ent.target);
        }
    })
})
var team = document.getElementsByClassName('teamImg')[0]
var img = document.getElementsByClassName("inImg")[0];
var img2 = document.getElementsByClassName("teamImg")[1];
observer1.observe(img)
observer1.observe(team);
observer1.observe(img2);