// static/script.js 
// JavaScript for Smart Mirror Chatbot
// Handles chat functionality, sending messages, and displaying structured responses.

// ✅ Load Markdown converter (for bold, code blocks, etc.)
const markdownConverter = window.marked || { parse: (text) => text };

// Select chat elements
const chat = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');

function scrollToBottom(container = chat) {
    if (!container) return;
    container.scrollTop = container.scrollHeight;
}

// ✅ Handle chat form submit (main chat box)
if (form) {
    form.onsubmit = async (e) => {
        e.preventDefault();
        const userMsg = input?.value.trim();
        if (!userMsg) return;

        // Display user message
        if (chat) {
            chat.innerHTML += `<div class="user"><b style="color:black">You:</b> ${userMsg}</div>`;
            scrollToBottom();
        }
if (input) {
    input.value = "";
    autoResize();      // Shrink textarea back to one line
}
        try {
           const formData = new FormData();

formData.append("message", userMsg);

if(selectedPDF){
    formData.append("pdf", selectedPDF);
}

if(selectedImage){
    formData.append("image", selectedImage);
}
const res = await fetch("/chat",{
    method:"POST",
    body:formData
});

            const data = await res.json();
           selectedPDF = null;
selectedImage = null;

pdfInput.value = "";
imageInput.value = "";

            // ✅ Clean and format Jobby’s response
            let botReply = data.response || "Sorry, no response.";
            
            // Ensure consistent “Jobby:” label at start
            if (!botReply.trim().startsWith("Jobby:")) {
                botReply = "Jobby:".fontcolor("black").bold() + " " + botReply.trim();
            }

            // ✅ Display formatted markdown with proper spacing
            const formattedReply = markdownConverter.parse(botReply)
                .replace(/<pre><code/g, '<pre class="code-block"><code')
                .replace(/\n/g, "<br>");

            if (chat) {
              chat.innerHTML += `
<div class="bot">
    <div class="bot-message" style="line-height:1;font-size:18px;">
        ${formattedReply}
    </div>

    <button class="speak-btn" onclick="speakMessage(this)">
        <i id="voiceup" class="fa-solid fa-volume-high"></i>
    </button>
</div>
`;
                scrollToBottom();
            }
        } catch (error) {
            if (chat) {
                chat.innerHTML += `<div class="bot"><b>Jobby:</b> Sorry, an error occurred.</div>`;
                scrollToBottom();
            }
        }
    };
}

// Focus input on page load
window.onload = () => {
    if (input) input.focus();
};

// Function to update current timestamp every second
function updateTimestamp() {
    const now = new Date();
    const options = { 
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    const tsEl = document.getElementById('current-timestamp');
    if (tsEl) tsEl.textContent = now.toLocaleString(undefined, options);
}

// Select chatbot elements
const chatbotContainer = document.getElementById('chatbot-container');
const chatbotIcon = document.querySelector('.chatbot-icon');

// Function to toggle chatbot visibility
function toggleChat() {
    if (!chatbotContainer) return;
    chatbotContainer.classList.toggle('hidden');
    chatbotContainer.classList.toggle('visible');
}

updateTimestamp();
setInterval(updateTimestamp, 1000);

// ✅ Clear chat history on page load
window.addEventListener('load', () => {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) chatMessages.innerHTML = '';
});

// ✅ Secondary chat function (for other UI)
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const message = userInput?.value.trim();

    if (!message) return;

    // Display user message
    const userMessage = document.createElement('div');
    userMessage.innerHTML =` <b>You:</b> ${message}`;
    if (chatMessages) chatMessages.appendChild(userMessage);

    // Clear input
    if (userInput) userInput.value = '';

    try {

    const formData = new FormData();

    formData.append("message", message);

    if(selectedPDF){
        formData.append("pdf", selectedPDF);
    }

    const response = await fetch("/chat",{
        method:"POST",
        body:formData
    });

    const data = await response.json();

 

    let botReply = data.response || "Sorry, no response.";

    if (!botReply.trim().startsWith("Jobby:")) {
        botReply = "Jobby: " + botReply.trim();
    }

    const formattedReply = markdownConverter.parse(botReply);

    const botMessage = document.createElement("div");

    botMessage.innerHTML = `
        <div class="bot">
            ${formattedReply}
        </div>
    `;

    chatMessages.appendChild(botMessage);

}
catch(error){
    console.log(error);
}
        // if (chatMessages) chatMessages.appendChild(errorMessage);
        
        // Scroll to bottom
        if (chatMessages){

         chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}
// Create Speech Recognition object
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();

// Settings
recognition.lang = "en-US";
recognition.continuous = false;
recognition.interimResults = false;
let micBTN = document.getElementById("micButton");
let ic = document.getElementById("icon");

micBTN.addEventListener("click", function () {
    ic.title = "Listening...";
    ic.style.color = "red";   // Change color while listening
    recognition.start();
});
recognition.onresult = function(event){

    input.value = event.results[0][0].transcript;

    autoResize();

};recognition.onend = function () {
    ic.title = "Click to start speaking";
    ic.style.color = "white";
};
recognition.onerror = function (event) {
    alert("Microphone Error: " + event.error);

    ic.title = "Click to start speaking";
    ic.style.color = "white";
};
function autoResize() {

    input.style.height = "auto";

    input.style.height = input.scrollHeight + "px";

}
input.addEventListener("input", autoResize);
input.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();   // Stop creating a new line

        form.requestSubmit();      // Submit the form

    }

});
let currentSpeech = null;
let speaking = false;

let selectedPDF = null;
let selectedImage = null;

function speakMessage(button) {

    // Stop if already speaking
    if (speaking) {
        speechSynthesis.cancel();
        speaking = false;

        button.innerHTML =
            '<i class="fa-solid fa-volume-high"></i>';

        return;
    }

    // Get only bot message
    
const botElement = button.parentElement.querySelector(".bot-message");

let message = "";

// Speak only normal text
botElement.childNodes.forEach(node => {

    // Ignore code blocks
    if (node.nodeName === "PRE") return;

    message += node.textContent + "\n";
});

message = message.replace(/^Jobby:\s*/i, "");

// Remove emojis
message = message.replace(
    /[\u{1F300}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu,
    ""
);

message = message.trim();
    // Create speech
    currentSpeech = new SpeechSynthesisUtterance(message);

    currentSpeech.lang = "en-US";

    // Load available voices
    const voices = speechSynthesis.getVoices();

    currentSpeech.voice =
        voices.find(v => v.lang.startsWith("en")) || voices[0];

    currentSpeech.rate = 1;
    currentSpeech.pitch = 1;

    speaking = true;

    button.innerHTML =
        '<i class="fa-solid fa-stop"></i>';

    currentSpeech.onend = function () {

        speaking = false;

        button.innerHTML =
            '<i class="fa-solid fa-volume-high"></i>';

    };

    speechSynthesis.speak(currentSpeech);
}

// Load voices
speechSynthesis.onvoiceschanged = () => {
    speechSynthesis.getVoices();
};
const plusBtn=document.getElementById("plusBtn");

const uploadMenu=document.getElementById("uploadMenu");

const imageOption=document.getElementById("imageOption");

const pdfOption=document.getElementById("pdfOption");

const imageInput=document.getElementById("imageInput");

const pdfInput=document.getElementById("pdfInput");
plusBtn.addEventListener("click", () => {
    console.log("Plus clicked");
    uploadMenu.classList.toggle("hidden");
});
imageOption.addEventListener("click",()=>{

    imageInput.click();

});
pdfOption.addEventListener("click",()=>{

    pdfInput.click();

});
imageInput.addEventListener("change", () => {

    const file = imageInput.files[0];

    if (!file) return;

    selectedImage = file;

    const url = URL.createObjectURL(file);

    chat.innerHTML += `
        <div class="user">
            <img src="${url}" style="width:180px;border-radius:10px;">
        </div>
    `;

    scrollToBottom();

    uploadMenu.classList.add("hidden");
});

pdfInput.addEventListener("change", () => {

    selectedPDF = pdfInput.files[0];

    if (!selectedPDF) return;

    chat.innerHTML += `
        <div class="user">
            📄 <b>${selectedPDF.name}</b>
        </div>
    `;

    scrollToBottom();

    uploadMenu.classList.add("hidden");

});

