const messagesBox = document.getElementById("messages");
const input = document.getElementById("question");

function addMessage(text, type) {
    const div = document.createElement("div");
    div.className = `msg ${type}`;
    div.textContent = text;
    messagesBox.appendChild(div);
    messagesBox.scrollTop = messagesBox.scrollHeight; // auto scroll
}

async function sendQuestion() {
    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");
    input.value = "";

    addMessage("Sơu đang trả lời...", "bot"); // loading tạm
    const loadingMsg = messagesBox.lastChild;

    const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
    });

    const data = await res.json();

    loadingMsg.textContent = data.answer;
    messagesBox.scrollTop = messagesBox.scrollHeight;
}

// Gửi bằng Enter
input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendQuestion();
});

const setHeight = () => {
    const height = window.visualViewport ? window.visualViewport.height : window.innerHeight;
    document.body.style.height = `${height}px`;
    document.querySelector('.chat-container').style.height = `${height}px`;
    
    messagesBox.scrollTop = messagesBox.scrollHeight;
};

if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', setHeight);
} else {
    window.addEventListener('resize', setHeight);
}


setHeight();