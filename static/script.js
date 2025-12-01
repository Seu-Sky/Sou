const messagesBox = document.getElementById("messages");
const input = document.getElementById("question");

function addMessage(text, type) {
    const div = document.createElement("div");
    div.className = `msg ${type}`;
    div.textContent = text;
    messagesBox.appendChild(div);
    messagesBox.scrollTop = messagesBox.scrollHeight;
}

async function sendQuestion() {
    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");
    input.value = "";

    addMessage("Sơu đang trả lời...", "bot");
    const loadingMsg = messagesBox.lastChild;

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });
        const data = await res.json();
        loadingMsg.textContent = data.answer;
    } catch (e) {
        loadingMsg.textContent = "Lỗi kết nối server!";
    }
    messagesBox.scrollTop = messagesBox.scrollHeight;
}


input.addEventListener("focus", () => {
    setTimeout(() => {
      
        input.scrollIntoView({ behavior: "smooth", block: "center" });
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }, 300); 
});


const setHeight = () => {

    const height = window.visualViewport ? window.visualViewport.height : window.innerHeight;
    
    document.body.style.height = `${height}px`;
    document.querySelector('.chat-container').style.height = `${height}px`;
    window.scrollTo(0, 0); 
    
    messagesBox.scrollTop = messagesBox.scrollHeight;
};

if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', setHeight);
} else {
    window.addEventListener('resize', setHeight);
}

setHeight();

// Gửi bằng Enter
input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendQuestion();
});