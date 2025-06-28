document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userMessage = userInput.value.trim();

        if (userMessage === '') {
            return;
        }

        appendMessage(userMessage, 'user');
        userInput.value = '';

        // Mock API call
        const botResponse = await getBotResponse(userMessage);
        appendMessage(botResponse, 'bot');
    });

    function appendMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', `${sender}-message`);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function getBotResponse(userMessage) {
        // In a real application, you would make an API call here.
        // For example:
        // const response = await fetch('/api/chat', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ message: userMessage })
        // });
        // const data = await response.json();
        // return data.reply;

        // Mocking the API response for demonstration.
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(`This is a mocked response to: "${userMessage}"`);
            }, 500);
        });
    }
}); 