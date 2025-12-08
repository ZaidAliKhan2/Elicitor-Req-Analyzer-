const API_BASE = "http://127.0.0.1:8000";

// Add this logic to the top of your existing ui/app.js file

const authStatusContainer = document.getElementById("authStatusContainer");
const loggedInUserContainer = document.getElementById("loggedInUserContainer");
const navLoginBtn = document.getElementById("navLoginBtn");
const navSignupBtn = document.getElementById("navSignupBtn");
const logoutBtn = document.getElementById("logoutBtn");
const userNameDisplay = document.getElementById("userNameDisplay");
const sidebarAvatar = document.getElementById("sidebarAvatar");
const greetingDiv = document.getElementById("greeting");
const greetingTextDiv = document.getElementById("greetingText");

// Function to update the UI based on auth status
function updateAuthUI() {
  const token = localStorage.getItem("authToken");
  const userName = localStorage.getItem("userName");

  const isLoggedIn = !!token;
  navLoginBtn.style.display = isLoggedIn ? "none" : "inline-block";
  navSignupBtn.style.display = isLoggedIn ? "none" : "inline-block";
  loggedInUserContainer.style.display = isLoggedIn ? "flex" : "none";

  if (isLoggedIn) {
    // Logged In State: Use personalized greeting
    userNameDisplay.textContent = `Hello, ${userName || "User"}`;
    initUserMode(userName);
  } else {
    initGuestMode();
  }
  initializeChatSystem();
}

// --- PROJECT SETUP FIX: New Initialization Function ---
function initializeChatSystem() {
  // This function encapsulates the logic that should run on page load for all users
  chatInput.disabled = true;
  chatInput.placeholder = "Please set up your project first...";
  sendBtn.disabled = true;

  // Only show the welcome message once if chat history is empty
  if (chatArea.children.length === 0) {
    appendMessage(
      "👋 Hi — I'm Elicitor, your requirements analyzer. Let me help you set up your project first.",
      "assistant"
    );
    showProjectSetup();
  }
}
// Add the logout event listener
logoutBtn.addEventListener("click", () => {
  // Clear all auth related storage
  localStorage.removeItem("authToken");
  localStorage.removeItem("userName");
  localStorage.removeItem("userEmail");

  // Update the UI immediately
  updateAuthUI();

  // Redirect to login page to prevent unauthorized API use if guest access is not intended
  window.location.href = "components/login.html";
});

document.addEventListener("DOMContentLoaded", updateAuthUI);

// Cached DOM
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const chatArea = document.getElementById("chatArea");
const greeting = document.getElementById("greeting");
const topBar = document.getElementById("topBar");
const projectBadge = document.getElementById("projectBadge");
const newChatBtn = document.getElementById("newChatBtn");
const changeDomainBtn = document.getElementById("changeDomainBtn");
const endConversationBtn = document.getElementById("endConversationBtn");
let isProjectSet = false;

let currentProject = null;
let projectSetupShown = false;

const guestGreetings = [
  "Welcome, Stranger 👋",
  "Hello, Mystery Guest 🎭",
  "Greetings, Wanderer 🌟",
  "Hey there, Anonymous 🕶️",
  "Welcome, Visitor 👤",
];
// --- TIME-BASED GREETING ARRAYS ---

const morningGreetings = [
  "Good Morning, early bird 🌤️",
  "Rise and shine, ready to analyze? ☕",
  "Morning! Let's get to work 💻",
];

const afternoonGreetings = [
  "Good Afternoon, focused analyst! 📝",
  "Welcome back, ready for the next task?",
  "Hello! Requirements await your review.",
];

const eveningGreetings = [
  "Good Evening, Elicitor is here to help 🌙",
  "Wrapping up the day? Let's analyze a few more.",
  "Twilight greetings! Ready for analysis.",
];

const nightGreetings = [
  "Hello Night Owl 🦉, ready for late-night analysis.",
  "Still working? Let's classify those requirements. 💡",
  "Shhh... it's quiet. Time for deep analysis.",
]; // --- TIME SELECTOR HELPER ---

function getTimeBasedGreeting() {
  const hour = new Date().getHours();

  if (hour >= 5 && hour < 12) {
    // 5 AM to 11:59 AM
    return morningGreetings;
  } else if (hour >= 12 && hour < 17) {
    // 12 PM to 4:59 PM
    return afternoonGreetings;
  } else if (hour >= 17 && hour < 22) {
    // 5 PM to 9:59 PM
    return eveningGreetings;
  } else {
    // 10 PM to 4:59 AM
    return nightGreetings;
  }
}
const userIcon = `<svg viewBox="0 0 24 24" fill="currentColor" class="user-icon">
  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
</svg>`;

// --- GREETING LOGIC ---

function initGuestMode() {
  // 1. Random Greeting
  const randomGreeting =
    guestGreetings[Math.floor(Math.random() * guestGreetings.length)];
  document.getElementById("greetingText").innerHTML = randomGreeting;

  // 2. Generic Sidebar Avatar
  const sidebarAvatar = document.querySelector(".sidebar-avatar");
  sidebarAvatar.innerHTML = userIcon;
  sidebarAvatar.style.color = "#888";
  sidebarAvatar.style.backgroundColor = "#333";
}

// --- UPDATED initUserMode FUNCTION ---
// File: ui/app.js (Locate initUserMode)

function initUserMode(userName) {
  const sidebarAvatar = document.querySelector(".sidebar-avatar");
  const greetingTextDiv = document.getElementById("greetingText");
  const safeUserName = userName || "User";

  // 1. Determine Time and Select Random Greeting
  const availableGreetings = getTimeBasedGreeting();
  const randomGreeting =
    availableGreetings[Math.floor(Math.random() * availableGreetings.length)];

  // ⭐ CHANGE HERE: Ensure the greeting combines the time-based phrase with the full user name. ⭐
  // E.g., "Good Morning, early bird" becomes "Good Morning, Zaid Ali Khan"
  const greetingPhrase =
    randomGreeting.split(" ")[0] + " " + randomGreeting.split(" ")[1]; // Takes "Good Morning"

  // Handle specific, shorter greetings (like "Welcome Night Owl")
  let finalGreeting = `${greetingPhrase}, ${safeUserName}`;

  if (
    randomGreeting.includes("Night Owl") ||
    randomGreeting.includes("Stranger")
  ) {
    finalGreeting = `${
      randomGreeting.split(" ")[0]
    }, ${safeUserName} ${randomGreeting.split(" ").slice(2).join(" ")}`;
  } else {
    finalGreeting = `${greetingPhrase}, ${safeUserName}`;
  }

  // Set the main greeting text
  greetingTextDiv.innerHTML = `<span class="greeting-star"></span> ${finalGreeting}`;

  // 2. Personalized Sidebar Avatar (remains the same)
  const userAlias =
    safeUserName.charAt(0).toUpperCase() +
    safeUserName.split(" ").pop().charAt(0).toUpperCase();
  sidebarAvatar.textContent = userAlias;
  sidebarAvatar.style.color = "white";
  sidebarAvatar.style.backgroundColor = "var(--color-primary)";
}

//auto scroll to response code
function scrollToBottom() {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: "smooth",
  });
}

//typing animation function code
function showTypingIndicator() {
  const container = document.createElement("div");
  container.className = "typing-indicator";
  container.id = "typingIndicator";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar bot-avatar";
  const img = document.createElement("img");
  img.src = "ElicitorLogo.png";
  img.alt = "Elicitor";
  img.onerror = function () {
    avatar.textContent = "E";
  };
  avatar.appendChild(img);

  const dots = document.createElement("div");
  dots.className = "typing-dots";
  dots.innerHTML = `
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
  `;

  container.appendChild(avatar);
  container.appendChild(dots);
  chatArea.appendChild(container);
  scrollToBottom();
}

function hideTypingIndicator() {
  const indicator = document.getElementById("typingIndicator");
  if (indicator) {
    indicator.remove();
  }
}

//initializing project domain animation code
function showInitializingMessage() {
  const container = document.createElement("div");
  container.className = "typing-indicator";
  container.id = "initializingIndicator";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar bot-avatar";
  const img = document.createElement("img");
  img.src = "ElicitorLogo.png";
  img.alt = "Elicitor";
  img.onerror = function () {
    avatar.textContent = "E";
  };
  avatar.appendChild(img);

  const dots = document.createElement("div");
  dots.className = "typing-dots";
  dots.innerHTML = `
    <span style="color: var(--text-secondary); font-size: 14px; margin-right: 8px;">Initializing domain</span>
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
  `;

  container.appendChild(avatar);
  container.appendChild(dots);
  chatArea.appendChild(container);
  scrollToBottom();
}

function hideInitializingMessage() {
  const indicator = document.getElementById("initializingIndicator");
  if (indicator) {
    indicator.remove();
  }
}

function appendMessage(text, who = "assistant") {
  const container = document.createElement("div");
  container.className = "msg-container " + who;

  const avatar = document.createElement("div");
  avatar.className =
    "msg-avatar " + (who === "user" ? "user-avatar" : "bot-avatar");

  if (who === "user") {
    avatar.innerHTML = userIcon;
  } else {
    const img = document.createElement("img");
    img.src = "ElicitorLogo.png";
    img.alt = "Elicitor";
    img.onerror = function () {
      avatar.textContent = "E";
    };
    avatar.appendChild(img);
  }

  const div = document.createElement("div");
  div.className = "msg " + who;
  div.innerHTML = `<div>${escapeHtml(text)}</div>`;

  container.appendChild(avatar);
  container.appendChild(div);
  chatArea.appendChild(container);
  scrollToBottom();
  chatArea.scrollTop = chatArea.scrollHeight;
}

function appendAnalysisResult(data) {
  const container = document.createElement("div");
  container.className = "msg-container assistant";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar bot-avatar";
  const img = document.createElement("img");
  img.src = "ElicitorLogo.png";
  img.alt = "Elicitor";
  img.onerror = function () {
    avatar.textContent = "E";
  };
  avatar.appendChild(img);

  const scope = data.scope_check;
  const cls = data.classification;
  const confidence = (scope.best_score || 0) * 100;

  const resultDiv = document.createElement("div");
  resultDiv.className = "analysis-result";
  resultDiv.innerHTML = `
        <div class="analysis-header">
          <h3>📊 Requirement Analysis</h3>
        </div>
        
        <div class="analysis-section">
          <div class="analysis-label">Scope Status</div>
          <div class="scope-status ${
            scope.in_scope ? "in-scope" : "out-scope"
          }">
            <span>${scope.in_scope ? "✅" : "❌"}</span>
            <span>${scope.in_scope ? "In Scope" : "Out of Scope"}</span>
          </div>
          <div class="info-text">${escapeHtml(
            scope.message || "No additional information"
          )}</div>
        </div>

        <div class="analysis-section">
          <div class="analysis-label">Confidence Score</div>
          <div class="confidence-bar">
            <div class="confidence-fill" style="width: ${confidence}%"></div>
          </div>
          <div class="confidence-text">${confidence.toFixed(1)}% confident</div>
        </div>

        <div class="analysis-section">
          <div class="analysis-label">Classification</div>
          <div class="classification-badge ${cls.type?.toLowerCase()}">
            <span>${
              cls.type === "FR" ? "⚙️" : cls.type === "NFR" ? "⭐" : "❓"
            }</span>
            <span>${
              cls.type === "FR"
                ? "Functional Requirement"
                : cls.type === "NFR"
                ? "Non-Functional Requirement"
                : cls.type || "Unknown"
            }</span>
          </div>
          ${
            cls.sub_category
              ? `<div class="info-text">Subcategory: ${escapeHtml(
                  cls.sub_category
                )}</div>`
              : ""
          }
          ${
            cls.message
              ? `<div class="info-text">${escapeHtml(cls.message)}</div>`
              : ""
          }
        </div>
      `;

  container.appendChild(avatar);
  container.appendChild(resultDiv);
  chatArea.appendChild(container);
  scrollToBottom();
  chatArea.scrollTop = chatArea.scrollHeight;
}

function escapeHtml(str) {
  return String(str).replace(
    /[&<>"']/g,
    (m) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[
        m
      ])
  );
}

function showProjectSetup() {
  if (projectSetupShown) return;
  projectSetupShown = true;

  const setupCard = document.createElement("div");
  setupCard.className = "project-setup-card";
  setupCard.id = "projectSetupCard";
  setupCard.innerHTML = `
        <h3>🚀 Setup Your Project</h3>
        <p>Describe your project so I can better analyze requirements and check scope.</p>
        <textarea id="projectDescInline" placeholder="E.g., E-commerce platform for selling products with authentication, catalog, cart, and payments"></textarea>
        <div class="project-setup-buttons">
          <button id="skipProjectInline" class="btn-secondary">Use Default</button>
          <button id="submitProjectInline" class="btn-primary">Set Project</button>
        </div>
      `;
  chatArea.appendChild(setupCard);
  chatArea.scrollTop = chatArea.scrollHeight;

  document
    .getElementById("submitProjectInline")
    .addEventListener("click", () => {
      const desc =
        document.getElementById("projectDescInline").value.trim() ||
        "Default e-commerce platform for selling products with authentication, catalog, cart, and payments";
      setProject(desc);
      setupCard.remove();
    });

  document.getElementById("skipProjectInline").addEventListener("click", () => {
    const desc =
      "Default e-commerce platform for selling products with authentication, catalog, cart, and payments";
    setProject(desc);
    setupCard.remove();
  });
}

async function setProject(desc) {
  showInitializingMessage();
  const body = { project_description: desc };
  try {
    const res = await fetch(API_BASE + "/init_project", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const j = await res.json();

    hideInitializingMessage();
    if (j.ok) {
      currentProject = desc;
      isProjectSet = true;
      chatInput.disabled = false;
      sendBtn.disabled = false;
      projectBadge.textContent = j.domain || "Custom Project";
      topBar.style.display = "flex";
      greeting.style.display = "none";
      appendMessage(
        `✓ Project initialized successfully! Domain: ${
          j.domain || "custom project"
        }. I'm ready to analyze your requirements.`,
        "assistant"
      );
    } else {
      appendMessage("Failed to set project: " + JSON.stringify(j), "assistant");
    }
  } catch (err) {
    hideInitializingMessage();
    appendMessage("Backend error: " + err.toString(), "assistant");
  }
}
chatInput.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = Math.min(this.scrollHeight, 200) + "px";
});

async function sendRequirement(text) {
  appendMessage(text, "user");
  sendBtn.disabled = true;
  chatInput.disabled = true;
  showTypingIndicator();
  try {
    const res = await fetch(API_BASE + "/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ requirement: text }),
    });
    const j = await res.json();

    hideTypingIndicator();
    if (!j.ok) {
      appendMessage(
        "❌ Analysis failed: " + (j.detail || JSON.stringify(j)),
        "assistant"
      );
      return;
    }

    appendAnalysisResult(j.result);
  } catch (err) {
    hideTypingIndicator();
    appendMessage("❌ Network/backend error: " + err.toString(), "assistant");
  } finally {
    sendBtn.disabled = false;
    chatInput.disabled = false;
    chatInput.focus();
  }
}

chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = chatInput.value.trim();
  if (!text) return;
  chatInput.value = "";
  chatInput.style.height = "auto";
  sendRequirement(text);
});

chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;
    chatInput.value = "";
    chatInput.style.height = "auto";
    sendRequirement(text);
  }
});

newChatBtn.addEventListener("click", () => {
  if (confirm("Start a new conversation? Current chat will be cleared.")) {
    chatArea.innerHTML = "";
    currentProject = null;
    projectSetupShown = false;
    topBar.style.display = "none";
    greeting.style.display = "flex";
    appendMessage(
      "👋 Hi — I'm Elicitor, your requirements analyzer. Let me help you set up your project first.",
      "assistant"
    );
    showProjectSetup();
    isProjectSet = false;
    chatInput.disabled = true;
    sendBtn.disabled = true;
    chatInput.placeholder = "Please set up your project first...";
  }
});

changeDomainBtn.addEventListener("click", () => {
  projectSetupShown = false;
  appendMessage(
    "Let's change your project domain. Please provide a new project description:",
    "assistant"
  );
  showProjectSetup();
});

endConversationBtn.addEventListener("click", () => {
  if (confirm("End this conversation? All chat history will be cleared.")) {
    chatArea.innerHTML = "";
    currentProject = null;
    projectSetupShown = false;
    topBar.style.display = "none";
    greeting.style.display = "flex";
    appendMessage(
      "👋 Conversation ended. Ready to start fresh when you are!",
      "assistant"
    );
    isProjectSet = false;
    chatInput.disabled = true;
    sendBtn.disabled = true;
    chatInput.placeholder = "Please set up your project first...";
    showProjectSetup();
  }
});
//Documentation code for visibility
const docsBtn = document.getElementById("docsBtn");
const docsModal = document.getElementById("docsModal");
const docsClose = document.getElementById("docsClose");

docsBtn.addEventListener("click", () => {
  docsModal.classList.add("active");
});

docsClose.addEventListener("click", () => {
  docsModal.classList.remove("active");
});

docsModal.addEventListener("click", (e) => {
  if (e.target === docsModal) {
    docsModal.classList.remove("active");
  }
});
