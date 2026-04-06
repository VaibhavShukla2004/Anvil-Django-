
    function scaleToFit() {
        const canvas = document.getElementById('canvas');
        const windowWidth = window.innerWidth;
        const targetWidth = 1920;
        const targetHeight = 1080;

        // Scale design to fit browser width
        const scale = windowWidth / targetWidth;
        canvas.style.transform = `scale(${scale})`;

        // Fix the gap: Ensure following content starts exactly after the scaled canvas
        const scaledHeight = targetHeight * scale;
        canvas.style.marginBottom = (scaledHeight - targetHeight) + "px";
    }

    // Audio Function
    function playAnvilSound() {
        // Metallic 'ting' sound for anvil
        const audio = new Audio('https://www.soundjay.com/industrial/sounds/anvil-hit-01.mp3');
        audio.play().catch(e => console.log("Audio play blocked by browser. Interaction required."));
    }

    window.addEventListener('resize', scaleToFit);
    window.addEventListener('load', scaleToFit);



function startExperience() {
    const canvas = document.getElementById('canvas');
    const video = document.getElementById('/static/videos/cat1.mp4');
    const rollTarget = document.getElementById('rollTarget');
    
    // 1. Trigger the Roll immediately
    canvas.classList.add('canvas-active');
    playAnvilSound();

    // 2. Wait exactly 2.5s (matching your --speed)
    setTimeout(() => {
        if (video) {
            video.currentTime = 0;
            video.play();
            // Add a class instead of changing style.opacity
            canvas.classList.add('video-ready'); 
        }
        
        // Enable centered state and redirect
        rollTarget.classList.add('is-centered');
        rollTarget.onclick = function() {
            window.location.href = "/your-next-page-url/"; 
        };
    }, 2500); 
}

function resetExperience() {
    const canvas = document.getElementById('canvas');
    const video = document.getElementById('pookieVideo');
    const rollTarget = document.getElementById('rollTarget');
    
    canvas.classList.remove('canvas-active');
    canvas.classList.remove('video-ready');
    rollTarget.classList.remove('is-centered');
    rollTarget.onclick = null;

    if (video) {
        video.pause();
    }
}function startExperience() {
    const canvas = document.getElementById('canvas');
    const video = document.getElementById('pookieVideo');
    const rollTarget = document.getElementById('rollTarget');
    
    // 1. Trigger the Roll immediately
    canvas.classList.add('canvas-active');
    playAnvilSound();

    // 2. Wait exactly 2.5s (matching your --speed)
    setTimeout(() => {
        if (video) {
            video.currentTime = 0;
            video.play();
            // Add a class instead of changing style.opacity
            canvas.classList.add('video-ready'); 
        }
        
        // Enable centered state and redirect
        rollTarget.classList.add('is-centered');
        rollTarget.onclick = function() {
            window.location.href = "/your-next-page-url/"; 
        };
    }, 2500); 
}

function resetExperience() {
    const canvas = document.getElementById('canvas');
    const video = document.getElementById('pookieVideo');
    const rollTarget = document.getElementById('rollTarget');
    
    canvas.classList.remove('canvas-active');
    canvas.classList.remove('video-ready');
    rollTarget.classList.remove('is-centered');
    rollTarget.onclick = null;

    if (video) {
        video.pause();
    }
}

async function loadExercises() {
    try {
        const response = await fetch("http://127.0.0.1:8000/exercise/"); // adjust if your endpoint differs
        const data = await response.json();

        console.log("Exercises:", data);
    } catch (error) {
        console.error("Error fetching exercises:", error);
    }
}

window.addEventListener("load", () => {
    loadExercises();
});