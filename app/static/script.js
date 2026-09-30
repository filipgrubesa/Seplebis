
async function signup(){
    const response = await fetch("/signup", {
        method: "POST"
    });

    const data = await response.json();

    const responseElement = document.getElementById("signup");
    responseElement.innerHTML = `Username <u>${data.username}</u> Password <u>${data.password}</u>`;
    responseElement.hidden = false;
    document.getElementById("signupbutton").style.display = "none";
    document.getElementById("message").hidden = false;
}

async function login(){
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    const response = await fetch(`/login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`, {
        method: "POST",
        credentials: "include"
    });

    const data = await response.json();

    if (data.success){
        window.location.href = "/static/posts.html";
    } else{
        document.getElementById("incorrect").hidden = false;
    }

}