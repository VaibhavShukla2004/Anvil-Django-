// anvil/static/js/script.js

// 1. Core Scaling & Audio Functions
function scaleToFit() {
    const canvas = document.getElementById('canvas');
    if (!canvas) return;
    const windowWidth = window.innerWidth;
    const targetWidth = 1920;
    const targetHeight = 1080;
    const scale = windowWidth / targetWidth;
    canvas.style.transform = `scale(${scale})`;
    const scaledHeight = targetHeight * scale;
    canvas.style.marginBottom = (scaledHeight - targetHeight) + "px";
}

function playAnvilSound() {
    const audio = new Audio('/static/audio/anvil.mp3');
    audio.play().catch(e => console.log("Audio play blocked."));
}

// 2. Card Builder Helper
const createCard = (item, type) => `
    <div class="${type}-card">
        <div class="card-image">
            <img src="${item.image_url || 'https://via.placeholder.com/300x200?text=ANVIL+FITNESS'}" alt="${item.name}">
        </div>
        <div class="card-content">
            <h3 class="${type}-name">${item.name}</h3>
            <div class="${type}-tags">
                <span class="tag">${item.difficulty || 'N/A'}</span>
                <span class="tag">${item.type || 'N/A'}</span>
            </div>
            <p class="muscle-info"><strong>Target:</strong> ${item.primary_muscles ? item.primary_muscles.join(', ') : 'N/A'}</p>
        </div>
    </div>
`;

// 3. Main Initialization Logic
document.addEventListener('DOMContentLoaded', function() {
    const exContainer = document.getElementById('exerciseContainer');

    // Load Scaling
    scaleToFit();
    window.addEventListener('resize', scaleToFit);

    // Fetch and Display Exercises
    if (exContainer) {
        console.log("Fetching exercises...");
        fetch('/exercise/') 
            .then(res => {
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                return res.json();
            })
            .then(data => {
                console.log("Exercises received:", data.length);
                if (data.length === 0) {
                    exContainer.innerHTML = '<p style="color:white; font-family:VT323;">DATABASE_EMPTY</p>';
                    return;
                }
                // Inject cards into the container
                exContainer.innerHTML = data.map(ex => createCard(ex, 'exercise')).join('');
            })
            .catch(err => {
                console.error("Fetch Error:", err);
                exContainer.innerHTML = `<p style="color: red;">FETCH_ERROR: ${err.message}</p>`;
            });
    }
});


let currentPosition = 1; // 0: Left, 1: Center, 2: Right

function moveSlider(direction) {
    const left = document.getElementById('circleLeft');
    const center = document.getElementById('circleCenter');
    const right = document.getElementById('circleRight');
    
    // We update the classes manually based on a simple rotation
    if (direction === 'right') {
        // Shift classes: Left -> Center -> Right -> Left
        let leftClass = left.className;
        left.className = right.className;
        right.className = center.className;
        center.className = leftClass;
    } else {
        // Shift classes the other way
        let rightClass = right.className;
        right.className = left.className;
        left.className = center.className;
        center.className = rightClass;
    }
}

// Update the startExperience in main.html to point to this new page
function startExperience() {
    const canvas = document.getElementById('canvas');
    const video = document.getElementById('pookieVideo');
    const rollTarget = document.getElementById('rollTarget');
    
    console.log("Experience Started...");
    canvas.classList.add('canvas-active');
    playAnvilSound();

    setTimeout(() => {
        console.log("Animation Finished. Checking for video and target...");
        
        if (video) {
            video.currentTime = 0;
            video.play();
            canvas.classList.add('video-ready'); 
        }
        
        if (rollTarget) {
            console.log("Setting up redirect on rollTarget...");
            rollTarget.classList.add('is-centered');
            
            // Force z-index and cursor via JS to be sure
            rollTarget.style.zIndex = "999"; 
            rollTarget.style.cursor = "pointer";

            rollTarget.onclick = function() {
                console.log("Redirecting to selection...");
                window.location.href = "/selection/"; 
            };
        } else {
            console.error("rollTarget NOT FOUND in DOM!");
        }
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