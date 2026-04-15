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

// Auto-refreshing authenticated fetch helper
async function authFetch(url, options = {}) {
    const token = localStorage.getItem('anvilAccess');
    if (token) {
        options.headers = Object.assign({}, options.headers, { 'Authorization': 'Bearer ' + token });
    }
    let res = await fetch(url, options);

    if (res.status === 401 && localStorage.getItem('anvilRefresh')) {
        // Try to refresh the access token
        try {
            const refreshRes = await fetch('/auth/refresh/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: localStorage.getItem('anvilRefresh') })
            });
            if (refreshRes.ok) {
                const refreshData = await refreshRes.json();
                localStorage.setItem('anvilAccess', refreshData.access);
                options.headers['Authorization'] = 'Bearer ' + refreshData.access;
                res = await fetch(url, options); // retry with new token
            } else {
                // Refresh also failed — clear stale auth
                localStorage.removeItem('anvilAccess');
                localStorage.removeItem('anvilRefresh');
                localStorage.removeItem('anvilUsername');
            }
        } catch(_) {
            localStorage.removeItem('anvilAccess');
            localStorage.removeItem('anvilRefresh');
            localStorage.removeItem('anvilUsername');
        }
    }
    return res;
}

// 2. Card Builder Helper
const createCard = (item, type, exercisesMap = {}) => {
    if (type === 'workout') {
        const exObjects = (item.exercise_ids || []).map(id => exercisesMap[id]).filter(Boolean);
        
        return `
            <div class="workout-section" style="margin-bottom: 20px; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #FF4B4B; padding-bottom: 10px; margin-bottom: 20px;">
                    <h3 class="${type}-name" style="font-family: 'Minecraft', sans-serif; font-size: 24px; margin: 0; color: #fff; letter-spacing: 1px;">${item.name}</h3>
                    <div class="workout-meta" style="font-family: 'Inter', sans-serif; font-size: 14px; color: #ccc;">
                        <span style="color: #fff; background: rgba(255,75,75,0.2); padding: 4px 10px; border-radius: 5px; margin-right: 15px;">${item.type || 'N/A'}</span>
                        <strong>Focus:</strong> ${item.muscle_groups ? item.muscle_groups.join(', ') : 'N/A'} | 
                        <strong>Fatigue:</strong> ${item.total_fatigue ? item.total_fatigue.toFixed(1) : 'N/A'}
                    </div>
                </div>
                
                <div class="workout-exercises-row" style="display: flex; gap: 25px; overflow-x: auto; padding-bottom: 15px;">
                    ${exObjects.length > 0 
                        ? exObjects.map(ex => `<div style="min-width: 300px; max-width: 300px; flex-shrink: 0;">${createCard(ex, 'exercise')}</div>`).join('')
                        : '<p style="color: red; font-family: \'Minecraft\';">No exercises found.</p>'
                    }
                </div>
            </div>
        `;
    }

    const diff = item.difficulty ? item.difficulty.toLowerCase() : 'n/a';
    let diffColor = '#FF4B4B';
    let diffBg = 'rgba(255, 75, 75, 0.2)';
    
    if (diff === 'beginner') { 
        diffColor = '#4BFF91'; 
        diffBg = 'rgba(75, 255, 145, 0.2)'; 
    } else if (diff === 'intermediate') { 
        diffColor = '#FFA500'; 
        diffBg = 'rgba(255, 165, 0, 0.2)'; 
    } else if (diff === 'hard' || diff === 'advanced') { 
        diffColor = '#FF4B4B'; 
        diffBg = 'rgba(255, 75, 75, 0.2)'; 
    }

    const exType = item.type ? item.type.toLowerCase() : '';
    let typeColor = '#aaa';
    let typeBg = 'rgba(150, 150, 150, 0.15)';
    if (exType === 'compound') {
        typeColor = '#7EC8E3';
        typeBg = 'rgba(126, 200, 227, 0.15)';
    } else if (exType === 'isolation') {
        typeColor = '#2563AC';
        typeBg = 'rgba(37, 99, 172, 0.15)';
    }

    return `
        <div class="${type}-card">
            <div class="card-image">
                <img src="${item.image_url || 'https://via.placeholder.com/300x200?text=ANVIL+FITNESS'}" alt="${item.name}">
            </div>
            <div class="card-content">
                <h3 class="${type}-name">${item.name}</h3>
                <div class="${type}-tags">
                    <span class="tag" style="color: ${diffColor}; background: ${diffBg}; border: 1px solid ${diffColor};">${item.difficulty || 'N/A'}</span>
                    <span class="tag" style="color: ${typeColor}; background: ${typeBg}; border: 1px solid ${typeColor};">${item.type || 'N/A'}</span>
                </div>
                <p class="muscle-info"><strong>Target:</strong> ${item.primary_muscles ? item.primary_muscles.join(', ') : 'N/A'}</p>
            </div>
        </div>
    `;
};

// 3. Main Initialization Logic
document.addEventListener('DOMContentLoaded', function() {
    const exContainer = document.getElementById('exerciseContainer');
    const workoutContainer = document.getElementById('WorkoutContainer');

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

    // Fetch and Display Workouts
    if (workoutContainer) {
        console.log("Fetching workouts and exercises...");
        
        const fetchWorkouts = async () => {
            const res = await authFetch('/workout/');
            if (!res.ok) return [];
            return res.json();
        };
        
        Promise.all([
            fetch('/exercise/').then(res => res.json()),
            fetchWorkouts()
        ])
        .then(([exercises, workouts]) => {
            const exercisesMap = {};
            exercises.forEach(ex => {
                exercisesMap[ex.id] = ex;
            });

            if (!Array.isArray(workouts) || workouts.length === 0) {
                workoutContainer.innerHTML = '<p style="color:rgba(255,255,255,0.5); font-family:VT323; font-size:28px;">LOG IN TO SEE YOUR SAVED WORKOUTS</p>';
                return;
            }
            workoutContainer.innerHTML = workouts.map(w => createCard(w, 'workout', exercisesMap)).join('');
        })
        .catch(err => {
            console.error("Fetch Error:", err);
            workoutContainer.innerHTML = `<p style="color: red;">FETCH_ERROR: ${err.message}</p>`;
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
    
    // 6. Init Selection UI
    if(document.getElementById('circleCenter')) {
        // Reset wizard to step 1
        goToStep(1);
    }
    
    console.log("Experience Started...");
    canvas.classList.add('canvas-active');

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

    // Clear inline styles set by startExperience so the circle
    // no longer blocks clicks after rolling back off-screen
    rollTarget.style.zIndex = "";
    rollTarget.style.cursor = "";

    if (video) {
        video.pause();
        video.currentTime = 0;
    }
}

/* ============================================================
   AUTH PANEL — Login / Register / Account logic
   Uses the existing REST API at /auth/login/ and /auth/register/
   JWT tokens stored in localStorage
   ============================================================ */

// ---- Tab Switcher ----
function switchAuthTab(tab) {
    const loginForm    = document.getElementById('formLogin');
    const registerForm = document.getElementById('formRegister');
    const forgotForm   = document.getElementById('formForgotPwd');
    const tabLogin     = document.getElementById('tabLogin');
    const tabRegister  = document.getElementById('tabRegister');

    if (forgotForm) forgotForm.classList.add('hidden');

    if (tab === 'login') {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        tabLogin.classList.add('active');
        tabRegister.classList.remove('active');
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        tabRegister.classList.add('active');
        tabLogin.classList.remove('active');
    }
}

function showForgotPwd() {
    document.getElementById('formLogin').classList.add('hidden');
    document.getElementById('formRegister').classList.add('hidden');
    document.getElementById('formForgotPwd').classList.remove('hidden');
    
    // Remove active state from tabs
    document.getElementById('tabLogin').classList.remove('active');
    document.getElementById('tabRegister').classList.remove('active');
}

// ---- Show Auth Message ----
function showMsg(elId, text, type) {
    const el = document.getElementById(elId);
    if (!el) return;
    el.textContent = text;
    el.className = 'auth-message ' + type;
}

// ---- Render Account View ----
function renderAccountView(username) {
    document.getElementById('authGuest').classList.add('hidden');
    document.getElementById('authAccount').classList.remove('hidden');

    const usernameEl = document.getElementById('accountUsername');
    const avatarEl   = document.getElementById('accountAvatar');
    const sinceEl    = document.getElementById('accountSince');

    if (usernameEl) usernameEl.textContent = username.toUpperCase();
    if (avatarEl)   avatarEl.textContent   = username.charAt(0).toUpperCase();

    // Derive a "member since" from when the token was stored
    const storedDate = localStorage.getItem('anvilLoginDate');
    if (sinceEl && storedDate) {
        const d = new Date(storedDate);
        sinceEl.textContent = d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    } else if (sinceEl) {
        sinceEl.textContent = '—';
    }
}

// ---- Render Guest View ----
function renderGuestView() {
    document.getElementById('authAccount').classList.add('hidden');
    document.getElementById('authGuest').classList.remove('hidden');
}

// ---- Handle Login ----
async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;
    const btn      = document.getElementById('loginSubmitBtn');

    showMsg('loginMsg', '', '');
    btn.disabled = true;
    btn.textContent = 'FORGING...';

    try {
        const res = await fetch('/auth/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (!res.ok) {
            showMsg('loginMsg', data.error || 'Invalid credentials.', 'error');
            return;
        }

        // Store JWT tokens
        localStorage.setItem('anvilAccess',    data.access);
        localStorage.setItem('anvilRefresh',   data.refresh);
        localStorage.setItem('anvilUsername',  username);
        localStorage.setItem('anvilLoginDate', new Date().toISOString());

        showMsg('loginMsg', 'Welcome back, ' + username + '!', 'success');

        setTimeout(() => renderAccountView(username), 600);

    } catch (err) {
        showMsg('loginMsg', 'Network error. Try again.', 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'ENTER THE FORGE';
    }
}

// ---- Handle Register ----
async function handleRegister(e) {
    e.preventDefault();
    const username  = document.getElementById('regUsername').value.trim();
    const email     = document.getElementById('regEmail').value.trim();
    const password  = document.getElementById('regPassword').value;
    const password2 = document.getElementById('regPassword2').value;
    const btn       = document.getElementById('registerSubmitBtn');

    showMsg('registerMsg', '', '');

    if (password !== password2) {
        showMsg('registerMsg', 'Passwords do not match.', 'error');
        return;
    }
    if (password.length < 6) {
        showMsg('registerMsg', 'Password must be at least 6 characters.', 'error');
        return;
    }

    btn.disabled = true;
    btn.textContent = 'FORGING...';

    try {
        const res = await fetch('/auth/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            const firstError = Object.values(data)[0];
            const msg = Array.isArray(firstError) ? firstError[0] : (firstError || 'Registration failed.');
            showMsg('registerMsg', msg, 'error');
            return;
        }

        showMsg('registerMsg', 'Account created! Logging you in...', 'success');

        // Auto-login after registration
        setTimeout(() => autoLoginAfterRegister(username, password), 900);

    } catch (err) {
        showMsg('registerMsg', 'Network error. Try again.', 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'JOIN THE FORGE';
    }
}

// ---- Handle Forgot Password ----
async function handleForgotPwd(e) {
    e.preventDefault();
    const username    = document.getElementById('forgotUsername').value.trim();
    const email       = document.getElementById('forgotEmail').value.trim();
    const newPassword = document.getElementById('forgotNewPassword').value;
    const btn         = document.getElementById('forgotSubmitBtn');

    showMsg('forgotMsg', '', '');
    
    if (newPassword.length < 6) {
        showMsg('forgotMsg', 'Password must be at least 6 characters.', 'error');
        return;
    }

    btn.disabled = true;
    btn.textContent = 'FORGING...';

    try {
        const res = await fetch('/auth/forgot-password/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, new_password: newPassword })
        });

        const data = await res.json();

        if (!res.ok) {
            showMsg('forgotMsg', data.error || 'Password reset failed.', 'error');
            return;
        }

        showMsg('forgotMsg', 'Password reset successful!', 'success');
        
        // Go back to login after a delay
        setTimeout(() => {
            switchAuthTab('login');
            showMsg('forgotMsg', '', '');
            document.getElementById('formForgotPwd').reset();
        }, 1500);

    } catch (err) {
        showMsg('forgotMsg', 'Network error. Try again.', 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'RESET PASSWORD';
    }
}

async function autoLoginAfterRegister(username, password) {
    try {
        const res = await fetch('/auth/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.setItem('anvilAccess',    data.access);
            localStorage.setItem('anvilRefresh',   data.refresh);
            localStorage.setItem('anvilUsername',  username);
            localStorage.setItem('anvilLoginDate', new Date().toISOString());
            renderAccountView(username);
        }
    } catch (_) { /* fail silently — user can log in manually */ }
}

// ---- Handle Logout ----
function handleLogout() {
    localStorage.removeItem('anvilAccess');
    localStorage.removeItem('anvilRefresh');
    localStorage.removeItem('anvilUsername');
    localStorage.removeItem('anvilLoginDate');

    showMsg('accountMsg', 'See you next time!', 'success');
    setTimeout(() => {
        showMsg('accountMsg', '', '');
        renderGuestView();
        switchAuthTab('login');
    }, 900);
}

// ---- On Page Load: Restore Session ----
document.addEventListener('DOMContentLoaded', function () {
    const token    = localStorage.getItem('anvilAccess');
    const username = localStorage.getItem('anvilUsername');
    if (token && username) {
        renderAccountView(username);
    }
    
    // 6. Init Selection UI
    if(document.getElementById('circleCenter')) {
        // Reset wizard to step 1
        goToStep(1);
    }
});

/* ============================================================
   WORKOUT GENERATOR WIZARD
   ============================================================ */

function goToStep(stepNum) {
    const steps = [document.getElementById('step1'), document.getElementById('step2'), document.getElementById('step3')];
    if (!steps[0]) return; // Not on selection page

    steps.forEach((step, index) => {
        if (index + 1 === stepNum) {
            step.style.display = 'flex';
            // Slight delay to allow transition
            setTimeout(() => step.classList.add('active'), 10);
        } else {
            step.classList.remove('active');
            setTimeout(() => step.style.display = 'none', 400); // Matches CSS transition duration
        }
    });
}

function toggleCustomEq() {
    const customPanel = document.getElementById('customEquipmentPanel');
    if (!customPanel) return;
    
    // Check which radio is picked
    const eqRadios = document.getElementsByName('eq_type');
    let customSelected = false;
    for (let r of eqRadios) {
        if (r.checked && r.value === 'custom') customSelected = true;
    }
    
    if (customSelected) {
        customPanel.classList.remove('hidden');
    } else {
        customPanel.classList.add('hidden');
        // Clear custom checkboxes
        const checkboxes = customPanel.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(cb => cb.checked = false);
    }
}

async function handleForgeWorkout() {
    const msgDiv = document.getElementById('wizardMsg');
    const btn = document.querySelector('.wizard-btn.forge');
    
    showMsg('wizardMsg', '', '');
    
    // 1. Gather Muscles
    const muscleInputs = document.querySelectorAll('#step1 input[name="muscles"]:checked');
    const muscles = Array.from(muscleInputs).map(cb => cb.value);
    
    if (muscles.length === 0) {
        showMsg('wizardMsg', 'Please select at least one muscle group.', 'error');
        goToStep(1);
        return;
    }
    
    // 2. Gather Equipment
    const eqType = document.querySelector('input[name="eq_type"]:checked').value;
    let equipment = [];
    if (eqType === 'gym') {
        equipment = []; // Empty means all equipment available
    } else if (eqType === 'none') {
        equipment = ['bodyweight'];
    } else if (eqType === 'custom') {
        const customInputs = document.querySelectorAll('#customEquipmentPanel input[name="equipment"]:checked');
        equipment = Array.from(customInputs).map(cb => cb.value);
        if (equipment.length === 0) {
            showMsg('wizardMsg', 'Please select at least one custom equipment.', 'error');
            return;
        }
    }
    
    // 3. Number of Exercises
    let numExercises = parseInt(document.getElementById('numExercises').value, 10);
    if (isNaN(numExercises) || numExercises < 1 || numExercises > 20) {
        numExercises = 5;
    }
    
    const payload = {
        muscle_groups: muscles,
        equipment: equipment,
        num_exercises: numExercises
    };

    btn.disabled = true;
    btn.innerHTML = 'FORGING...';

    const token = localStorage.getItem('anvilAccess');
    const headers = { 'Content-Type': 'application/json' };
    if (token) {
        headers['Authorization'] = 'Bearer ' + token;
    }

    try {
        const res = await fetch('/workout/generate/', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            showMsg('wizardMsg', data.error || 'Failed to forge workout.', 'error');
            btn.disabled = false;
            btn.innerHTML = 'FORGE WORKOUT';
            return;
        }

        // Success! Store into session storage and redirect
        sessionStorage.setItem('tempGeneratedWorkout', JSON.stringify(data));
        window.location.href = '/workout/generated/';

    } catch (err) {
        showMsg('wizardMsg', 'Network error. Try again.', 'error');
        btn.disabled = false;
        btn.innerHTML = 'FORGE WORKOUT';
    }
}