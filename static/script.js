const chatBox = document.getElementById("chatBox");
const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const clearBtn = document.getElementById("clearChatBtn");

// Load full message history from backend
async function loadHistory() {
    try {
        const res = await fetch("/api/messages");
        const messages = await res.json();
        chatBox.innerHTML = "";
        messages.forEach(m => addMessage(m.role, m.content));
    } catch (err) {
        console.error("Failed to load history:", err);
    }
}

// Show a message
function addMessage(role, content) {
    const msg = document.createElement("div");
    msg.className = `message ${role}`;
    msg.textContent = content;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Submit message
chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;
    addMessage("user", message);
    userInput.value = "";
    try {
        const response = await fetch("/api/messages", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });
        if (response.ok) {
            const data = await response.json();
            addMessage("bot", data.content);
        } else {
            addMessage("bot", "⚠️ Error sending message.");
        }
    } catch (err) {
        addMessage("bot", "⚠️ Connection error.");
    }
});

// Dark mode toggle
const darkBtn = document.getElementById("darkModeBtn");
darkBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    darkBtn.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
});

// Settings modal
const settingsBtn = document.getElementById("settingsBtn");
const modal = document.getElementById("settingsModal");
const closeModal = document.getElementById("closeModal");

settingsBtn.addEventListener("click", () => modal.style.display = "block");
closeModal.addEventListener("click", () => modal.style.display = "none");
window.addEventListener("click", (e) => { 
    if (e.target === modal) modal.style.display = "none"; 
});

// Clear chat
clearBtn.addEventListener("click", async () => {
    if (!confirm("Are you sure you want to clear the chat?")) return;
    try {
        const res = await fetch("/api/clear", { method: "POST" });
        if (res.ok) {
            chatBox.innerHTML = "";
        } else {
            alert("Failed to clear chat.");
        }
    } catch (err) {
        console.error(err);
        alert("Error clearing chat.");
    }
});

// Load history on page load
window.onload = loadHistory;
