document.addEventListener("DOMContentLoaded", () => {
  const assistantToggle = document.getElementById("toggle-assistant");
  const assistantBox = document.getElementById("assistant-box");
  const chatBox = document.getElementById("chat-box");
  const input = document.getElementById("assistant-input");
  const sendBtn = document.getElementById("send-btn");

  // Toggle assistant visibility
  assistantToggle.onclick = () => {
    assistantBox.classList.toggle("open");
    chatBox.scrollTop = chatBox.scrollHeight;
  };

  // Handle sending a message
  sendBtn.onclick = async () => {
    const userMsg = input.value.trim();
    if (!userMsg) return;

    appendMessage("user", `🧑 ${userMsg}`);
    input.value = "";
    appendMessage("bot", `🤖 Typing...`, true); // temporary loading

    try {
      const res = await fetch("http://127.0.0.1:8000/ask-assistant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg })
      });

      const data = await res.json();
      removeLoading();
      appendMessage("bot", `🤖 ${data.reply}`);
    } catch (err) {
      removeLoading();
      appendMessage("bot", "⚠️ Error contacting assistant.");
    }
  };

  function appendMessage(sender, content, loading = false) {
    const msg = document.createElement("div");
    msg.className = `chat ${sender}`;
    msg.innerText = content;
    if (loading) msg.classList.add("loading");
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function removeLoading() {
    const loader = document.querySelector(".chat.bot.loading");
    if (loader) loader.remove();
  }
});
