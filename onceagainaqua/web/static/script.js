async function sendMessage() {
    const input = document.getElementById('message');
    const message = input.value;
    if (!message.trim()) return;

    const response = await fetch('/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });
    const data = await response.json();
    appendMessage(data);
    input.value = '';
}

function appendMessage(data) {
    const box = document.getElementById('chat-box');
    const entry = document.createElement('p');
    entry.innerText = `You: ${data.user} \nBot: ${data.bot}`;
    box.appendChild(entry);
}