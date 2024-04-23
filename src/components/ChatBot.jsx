import React, { useState, useEffect, useRef } from "react";
import logoMain from "../assets/logo_main.svg";
import plus from "../assets/plus-sign-vector-icon.webp";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrashAlt, faSave, faPlusCircle } from "@fortawesome/free-solid-svg-icons";
function ChatBot() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [userId] = useState(() => Math.random().toString(36).substring(7));
  const [apiUrl, setApiUrl] = useState("http://localhost:5000/chat"); // Default to SSH tunnel URL initially
  const chatHistoryRef = useRef(null);
  useEffect(() => {
    determineApiUrl(); // Check which API URL to use when the component mounts
  }, []);

  
  useEffect(() => {
    // Scroll to the bottom of the chat history container when chat history updates
    chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
  }, [chatHistory]);


  async function determineApiUrl() {
    const localStatusUrl = "http://10.72.8.178:5000/status"; // Local network status endpoint
    const localChatUrl = "http://10.72.8.178:5000/chat";
    const tunnelChatUrl = "http://localhost:5000/chat";
    try {
      const response = await fetch(localStatusUrl, { method: 'GET' });
      if (response.ok) {
        setApiUrl(localChatUrl); // If the status is OK, use the local URL
      } else {
        setApiUrl(tunnelChatUrl); // Otherwise, use the SSH tunnel URL
      }
    } catch (error) {
      setApiUrl(tunnelChatUrl); // Use the tunnel URL if there's an error reaching the status endpoint
      console.error("Error reaching local server, using tunnel URL:", error);
    }
  }

  const sendMessage = async () => {
  
    if (message.trim() === "") return;
    document.getElementById("rating").classList.add("hidden");
    const userMessage = { text: `${message}`, sender: "You" };
    setMessage("");

    setChatHistory(chatHistory => [...chatHistory, userMessage]);

    document.getElementById("loading").classList.remove("hidden");

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({ question: message, user_id: userId }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const responseData = await response.json();
      const botResponse = { text: `${responseData.reply}`, sender: "HossBot" };
      document.getElementById("rating").classList.remove("hidden");
      setChatHistory(chatHistory => [
        ...chatHistory,
        botResponse,
      ]);
    } catch (error) {
      console.error("Failed to send message:", error);
    } finally {
      document.getElementById("loading").classList.add("hidden");
    }
  };
  function scrollToBottom() {
    const chatHistoryEl = document.getElementById("chatHistory");
    if (chatHistoryEl) {
      chatHistoryEl.scrollTop = chatHistoryEl.scrollHeight;
    }
  }


  function saveChat(user_rating) {
    document.getElementById("rating").classList.add("hidden");
    const userInputs = Array.from(
      document.querySelectorAll(".message.You")
    ).map((input) => input.textContent);
    const botInputs = Array.from(document.querySelectorAll(".message.HossBot")).map(
      (input) => input.textContent
    );
    const bot = document.querySelectorAll(".message.HossBot");
    const user = document.querySelectorAll(".message.You");
    for(let u of user){
      u.classList.remove("message");
    }
    for(let b of bot){
      b.classList.remove("message");
    }
    fetch("http://10.72.8.178:5000/save_chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        user_inputs: userInputs,
        bot_inputs: botInputs,

      }),
    })
    
      .then((response) => {
        console.log(response);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Chat saved successfully:", data);
      })
      .catch((error) => {
        console.error("Failed to save chat:", error);
      });
  }

  function clearChat() {
    const parent = document.getElementById("chatHistory");
    const children = parent.children;
    Array.from(children).forEach(function (child) {
      child.classList.add("hidden");
    });
    saveChat("000");
  }

  return (
    <div className="w-full flex justify-center items-center bg-hsu bg-center bg-no-repeat h-screen">
    <div className="flex justify-center items-start bg-opacity-50 pt-8 min-h-screen p-4 w-3/4" style={{ "--bg-purple": "var(--custom-purple)" }}>
      <div className="w-full max-w-3xl flex flex-col h-[70vh] bg-white rounded-xl shadow-2xl">
        <div className="flex justify-between items-center p-4 text-white rounded-t-xl" style={{ backgroundColor: "var(--bg-purple)" }}>
          <div className="flex items-center">
            <img src={logoMain} alt="Logo" className="w-15 h-12 mr-3" />
            <h1 className="text-lg font-bold">ChatBot</h1>
          </div>
          <div>
            <button
              onClick={clearChat}
              className="mr-2 bg-red-500 hover:bg-red-700 transition duration-300 ease-in-out text-white font-bold py-2 px-4 rounded-full shadow-lg hover:shadow-xl"
            >
              <FontAwesomeIcon icon={faPlusCircle} /> New Chat
            </button>
          </div>
        </div>
        <div id="chatHistory" className="flex-grow overflow-auto p-4 bg-gray-100" ref={chatHistoryRef}>
          {chatHistory.map((chat, index) => (
                <div key={index} className={`message ${chat.sender} ${chat.sender ==='You' ? 'rounded-r-lg': 'rounded-l-lg ml-auto'} rounded-b-lg  bg-[#D8D8D8] text-purple w-fit max-w-1/2  flex`}>
                <b>{chat.sender}:</b> <br />
                {chat.text}
                <br />
              </div>
              ))}
          <div id="loading" className="hidden ml-auto">
            <div className="typing-indicator">
              <div></div>
              <div></div>
              <div></div>
            </div>
          </div>
          <div id="rating" className="text-right rtl:text-right hidden">
                <div className="flex w-1/4 ml-auto justify-evenly">
                  <div className="bg-purple w-1/4 flex justify-center rounded-lg">
                    <button id="thumbsUpBtn" className="thumbs-up" onClick={() =>saveChat("100")}>👍</button>
                  </div>
                  <div className="bg-purple w-1/4 flex justify-center rounded-lg">
                    <button id="thumbsDownBtn" className="thumbs-down" onClick={() =>saveChat("010")}>👎</button>
                  </div>
                  <div className="bg-purple w-1/4 flex justify-center rounded-lg">
                    <button id="inappropriateBtn" className="inappropriate" onClick={() =>saveChat("001")}>❗</button>
                  </div>
                </div>
            </div>
          </div>
        <div className="p-4 bg-gray-200 rounded-b-xl">
          <textarea id="input-box" value={message} onChange={(e) => setMessage(e.target.value)} onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }}} className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:ring focus:ring-purple-200 resize-none transition duration-300 ease-in-out text-gray-900" placeholder="Type your message here..."></textarea>
          <button onClick={sendMessage} className="mt-2 w-full hover:bg-purple-700 transition duration-300 ease-in-out text-white font-bold py-2 px-4 rounded-lg shadow hover:shadow-md" style={{ backgroundColor: "var(--bg-purple)" }}>
            Send
          </button>
        </div>
        </div>
      </div>
    </div>
  );
}

export default ChatBot;

