import React, { useState, useEffect } from "react";
import logoMain from "../assets/logo_main.svg";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrashAlt, faSave } from "@fortawesome/free-solid-svg-icons";
import { useBeforeunload } from 'react-beforeunload';

function ChatBot() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [userId] = useState(() => Math.random().toString(36).substring(7));
  const [apiUrl, setApiUrl] = useState("http://localhost:5000/chat"); // Default to SSH tunnel URL initially

  useEffect(() => {
    determineApiUrl(); // Check which API URL to use when the component mounts
  }, []);

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

    const userMessage = { text: `You: ${message}`, sender: "user" };
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
      const botResponse = { text: `HossBot: ${responseData.reply}`, sender: "bot" };
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


  function saveChat(user_rating) {
    userInput[0].classList.remove("message");
    document.getElementById("rating").classList.add("hidden");
    const userInputs = Array.from(
      document.querySelectorAll(".message.You")
    ).map((input) => input.textContent);
    const botInputs = Array.from(document.querySelectorAll(".message.HossBot")).map(
      (input) => input.textContent
    );
    const bot = document.querySelectorAll(".message.HossBot");
    const user = document.querySelectorAll(".message.You");
    for(u of user){
      u.classList.remove("message");
    }
    for(b of bot){
      b.classList.remove("message");
    }
    fetch("http://localhost:5000/save_chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_inputs: userInputs,
        bot_inputs: botInputs,
        rating: user_rating,
      }),
    })
      .then((response) => {
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

  function saveChat(user_rating) {
    userInput[0].classList.remove("message");
    document.getElementById("rating").classList.add("hidden");
    const userInputs = Array.from(
      document.querySelectorAll(".message.You")
    ).map((input) => input.textContent);
    const botInputs = Array.from(document.querySelectorAll(".message.HossBot")).map(
      (input) => input.textContent
    );
    const bot = document.querySelectorAll(".message.HossBot");
    const user = document.querySelectorAll(".message.You");
    for(u of user){
      u.classList.remove("message");
    }
    for(b of bot){
      b.classList.remove("message");
    }
    fetch("http://localhost:5000/save_chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_inputs: userInputs,
        bot_inputs: botInputs,
        rating: user_rating,
      }),
    })
      .then((response) => {
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
    setChatHistory([]);
  }

  return (
    <div className="flex justify-center items-start bg-purple-600 bg-opacity-50 pt-8 min-h-screen p-4" style={{ "--bg-purple": "var(--custom-purple)" }}>
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
              <FontAwesomeIcon icon={faTrashAlt} /> New Chat
            </button>
            <button className="bg-green-500 hover:bg-green-700 transition duration-300 ease-in-out text-white font-bold py-2 px-4 rounded-full shadow-lg hover:shadow-xl">
              <FontAwesomeIcon icon={faSave} /> Save
            </button>
          </div>
        </div>
        <div id="chatHistory" className="flex-grow overflow-auto p-4 bg-gray-100">
          {chatHistory.map((chat, index) => (
                <div key={index} className={`message ${chat.sender} ${chat.sender ==='You' ? 'rounded-r-lg': 'rounded-l-lg ml-auto'} rounded-b-lg  bg-[#D8D8D8] text-purple w-fit  flex`}>
                <b>{chat.sender}:</b> <br />
                {chat.text}
                <br />
              </div>
              ))}
          <div id="loading" className="hidden">
            <div className="typing-indicator">
              <div></div>
              <div></div>
              <div></div>
            </div>
          </div>
          <div id="rating" className="text-right rtl:text-right">
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
  );
}

export default ChatBot;

