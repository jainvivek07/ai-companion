const chatHistory = document.getElementById('chat-history');
const msgInput = document.getElementById('msg-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const sidebar = document.getElementById('sidebar');

let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// --- UI Helpers ---
function toggleSidebar() {
    sidebar.classList.toggle('open');
    // For desktop, we might want to toggle 'collapsed' class instead if we implemented that logic
    if (window.innerWidth > 768) {
        sidebar.classList.toggle('collapsed');
    }
}

function scrollToBottom() {
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function addMessage(text, sender, persona = null) {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    
    let avatarUrl = sender === 'ai' 
        ? `https://api.dicebear.com/9.x/avataaars/svg?seed=${persona || 'Girlfriend'}`
        : `https://api.dicebear.com/9.x/avataaars/svg?seed=User`;

    div.innerHTML = `
        <img src="${avatarUrl}" class="avatar">
        <div class="bubble">${text}</div>
    `;
    chatHistory.appendChild(div);
    scrollToBottom();
}

function playAudio(b64Data) {
    const audio = new Audio("data:audio/mp3;base64," + b64Data);
    audio.play();
}

// --- API Calls ---
async function setPersona(persona) {
    const formData = new FormData();
    formData.append('persona', persona);
    
    const res = await fetch('/set_persona', { method: 'POST', body: formData });
    const data = await res.json();
    
    // Clear chat UI
    chatHistory.innerHTML = '';
    
    // Add Greeting
    addMessage(data.greeting, 'ai', persona);
    
    // Update Active State in Menu
    document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active'));
    document.getElementById(`p-${persona.replace(/\s+/g, '')}`).classList.add('active');
    
    // Close sidebar on mobile
    if (window.innerWidth <= 768) toggleSidebar();
}

async function clearChat() {
    await fetch('/reset', { method: 'POST' });
    chatHistory.innerHTML = '';
    addMessage("Chat cleared.", 'ai', getCurrentPersona());
}

function getCurrentPersona() {
    const active = document.querySelector('.menu-item.active');
    return active ? active.innerText.trim() : 'Girlfriend';
}

async function sendMessage() {
    const text = msgInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    msgInput.value = '';

    const formData = new FormData();
    formData.append('message', text);

    try {
        const res = await fetch('/chat', { method: 'POST', body: formData });
        const data = await res.json();
        addMessage(data.text, 'ai', getCurrentPersona());
        if (data.audio) playAudio(data.audio);
    } catch (e) {
        console.error(e);
    }
}

async function sendVoice(blob) {
    addMessage("🎤 (Sending Voice...)", 'user');
    
    const formData = new FormData();
    formData.append('audio', blob);

    try {
        const res = await fetch('/voice', { method: 'POST', body: formData });
        const data = await res.json();
        
        // Replace placeholder
        chatHistory.lastElementChild.querySelector('.bubble').innerText = "🎤 (Voice Message)";
        
        addMessage(data.text, 'ai', getCurrentPersona());
        if (data.audio) playAudio(data.audio);
    } catch (e) {
        console.error(e);
    }
}

// --- Event Listeners ---
sendBtn.onclick = sendMessage;
msgInput.onkeypress = (e) => { if (e.key === 'Enter') sendMessage(); };

micBtn.onclick = async () => {
    if (!isRecording) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
            mediaRecorder.onstop = () => {
                const blob = new Blob(audioChunks, { type: 'audio/wav' });
                sendVoice(blob);
            };
            
            mediaRecorder.start();
            isRecording = true;
            micBtn.classList.add('mic-active');
        } catch (e) {
            alert("Microphone access denied");
        }
    } else {
        mediaRecorder.stop();
        isRecording = false;
        micBtn.classList.remove('mic-active');
    }
};
