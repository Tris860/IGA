// script.js
function toggleForm() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
  
    if (loginForm.style.display === 'none') {
      loginForm.style.display = 'block';
      registerForm.style.display = 'none';
    } else {
      loginForm.style.display = 'none';
      registerForm.style.display = 'block';
    }
}


const dynamicText = document.querySelector(".hero-words h2 #typer");
const words = ["Success", "All...."];

// Variables to track the position and deletion status of the word
let wordIndex = 0;
let charIndex = 0;
let isDeleting = false;

const typeEffect = () => {
    const currentWord = words[wordIndex];
    const currentChar = currentWord.substring(0, charIndex);
    dynamicText.textContent = currentChar;
    dynamicText.classList.add("stop-blinking");

    if (!isDeleting && charIndex < currentWord.length) {
        // If condition is true, type the next character
        charIndex++;
        setTimeout(typeEffect, 200);
    } else if (isDeleting && charIndex > 0) {
        // If condition is true, remove the previous character
        charIndex--;
        setTimeout(typeEffect, 100);
    } else {
        // If word is deleted then switch to the next word
        isDeleting = !isDeleting;
        dynamicText.classList.remove("stop-blinking");
        wordIndex = !isDeleting ? (wordIndex + 1) % words.length : wordIndex;
        setTimeout(typeEffect, 1200);
    }
}

typeEffect();
function error_hide() {
    var message=document.getElementById("Error").innerText;
    errorBox=document.getElementById("Error");
    errorBox.style.animation='moveup 1s ease-in 1s '
    if(message.includes('verified') || message.includes('Verification')){
            errorBox.addEventListener('animationend', () => { 
                var verifyBox=document.getElementById("verify");
                errorBox.style.display = 'none'; 
                verifyBox.style.display='block';
        });
    }
    else{
        errorBox.addEventListener('animationend', () => { 
            errorBox.style.display = 'none'; 
        });
    }
    
}
function verifyBox_hide(){
   
    var verifyBox=document.getElementById("verify");
    verifyBox.style.animation='focus 2s ease-in 1s reverse ';
    verifyBox.addEventListener('animationend', () => {
        verifyBox.style.display='none';
    });


}

