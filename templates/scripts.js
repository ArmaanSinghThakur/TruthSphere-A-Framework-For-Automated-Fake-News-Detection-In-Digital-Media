function detectFakeNews() {
    const url = document.getElementById('newsUrl').value;
    // Placeholder for actual fake news detection logic
    document.getElementById('newsResult').innerText = `Checking ${url}... (This is a placeholder)`;
}

function detectFakeVideo() {
    const file = document.getElementById('videoFile').files[0];
    // Placeholder for actual AI-generated video detection logic
    document.getElementById('videoResult').innerText = `Checking ${file.name}... (This is a placeholder)`;
}

function detectFakePhoto() {
    const file = document.getElementById('photoFile').files[0];
    // Placeholder for actual AI-generated photo detection logic
    document.getElementById('photoResult').innerText = `Checking ${file.name}... (This is a placeholder)`;
}

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Placeholder for actual login logic
    if (username === 'admin' && password === 'password') {
        document.getElementById('loginResult').innerText = 'Login successful!';
    } else {
        document.getElementById('loginResult').innerText = 'Invalid username or password.';
    }
});



const btnHam = document.querySelector('.ham-btn');
const btnTimes = document.querySelector('.times-btn');
const navBar = document.getElementById('nav-bar');

btnHam.addEventListener('click', function(){
    if(btnHam.className !== ""){
        btnHam.style.display = "none";
        btnTimes.style.display = "block";
        navBar.classList.add("show-nav");
    }
})

btnTimes.addEventListener('click', function(){
    if(btnHam.className !== ""){
        this.style.display = "none";
        btnHam.style.display = "block";
        navBar.classList.remove("show-nav");
    }
})