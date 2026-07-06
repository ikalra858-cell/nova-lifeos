import { useState, useEffect, useRef } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activePage, setActivePage] = useState("chat");
  const [tasks, setTasks] = useState([]);
  const [notes, setNotes] = useState([]);
  const [events, setEvents] = useState([]);
  const [goals, setGoals] = useState([]);

  const [listening, setListening] = useState(false);

  const chatEndRef = useRef(null);

  const [dashboard, setDashboard] = useState({
  tasks: 0,
  notes: 0,
  events: 0,
  goals: 0,
});

  const loadDashboard = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/dashboard");
      setDashboard(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  const loadTasks = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/tasks");
    setTasks(res.data);
  } catch (err) {
    console.log(err);
  }
};

const loadNotes = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/notes");
    setNotes(res.data);
  } catch (err) {
    console.log(err);
  }
};

const loadEvents = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/events");
    setEvents(res.data);
  } catch (err) {
    console.log(err);
  }
};

const loadGoals = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/goals");
    setGoals(res.data);
  } catch (err) {
    console.log(err);
  }
};

  useEffect(() => {
  loadDashboard();
  loadTasks();
  loadNotes();
  loadEvents();
  loadGoals();
}, []);

  useEffect(() => {
  chatEndRef.current?.scrollIntoView({
    behavior: "smooth",
  });
}, [messages]);


useEffect(() => {
  chatEndRef.current?.scrollIntoView({
    behavior: "smooth",
  });
}, [messages]);


const startListening = () => {
  if (!("webkitSpeechRecognition" in window)) {
    alert("Speech Recognition is not supported in this browser.");
    return;
  }

  const recognition = new window.webkitSpeechRecognition();

  recognition.lang = "en-US";
  recognition.continuous = false;
  recognition.interimResults = false;

  setListening(true);

  recognition.start();

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    setMessage(text);
  };

  recognition.onend = () => {
    setListening(false);
  };
};

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = {
      sender: "You",
      text: message,
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
     }),
  };

    const currentMessage = message;
    setMessage("");

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:5000/chat", {
        message: currentMessage,
      });
      const novaMessage = {
        sender: "NOVA",
        text: res.data.reply,
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
      }),
    };

      setMessages((prev) => [...prev, novaMessage]);

      await loadDashboard();
      await loadTasks();
      await loadNotes();
      await loadEvents();
      await loadGoals();
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          sender: "NOVA",
          text: "Something went wrong.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex">

      {/* Sidebar */}

      <div className="w-72 h-screen sticky top-0 bg-zinc-900/95 backdrop-blur-xl border-r border-zinc-800 p-6 overflow-y-auto shadow-2xl">

        <h1 className="text-3xl font-bold text-purple-500">
          🌌 NOVA
        </h1>

        <p className="text-zinc-400 mt-2">
          AI Life Operating System
        </p>

        <div className="mt-10 space-y-3">

          <button
            onClick={() => {
            setActivePage("chat");

            setTimeout(() => {
            chatEndRef.current?.scrollIntoView({
            behavior: "smooth",
          });
        }, 100);
      }}
            className={`w-full text-left rounded-xl p-4 ${
            activePage === "chat"
            ? "bg-purple-600"
            : "bg-zinc-800 hover:bg-zinc-700"
        }`}
        >
          💬 Chat
        </button>

          <button
            onClick={() => setActivePage("tasks")}
           className={`w-full text-left rounded-xl p-4 transition-all duration-300 ${
  activePage === "tasks"
    ? "bg-gradient-to-r from-purple-600 to-indigo-600 shadow-lg scale-105"
    : "bg-zinc-800 hover:bg-zinc-700 hover:scale-105"
}`}
        >
           📌 Tasks ({dashboard.tasks})
          </button>

          <button
            onClick={() => setActivePage("notes")}
           className={`w-full text-left rounded-xl p-4 transition-all duration-300 ${
  activePage === "notes"
    ? "bg-gradient-to-r from-purple-600 to-indigo-600 shadow-lg scale-105"
    : "bg-zinc-800 hover:bg-zinc-700 hover:scale-105"
}`}
        >
            📝 Notes ({dashboard.notes})
          </button>

          <button
            onClick={() => setActivePage("events")}
            className={`w-full text-left rounded-xl p-4 transition-all duration-300 ${
  activePage === "calendar"
    ? "bg-gradient-to-r from-purple-600 to-indigo-600 shadow-lg scale-105"
    : "bg-zinc-800 hover:bg-zinc-700 hover:scale-105"
}`}
        >
            📅 Calendar ({dashboard.events})
          </button>

         <button
            onClick={() => setActivePage("goals")}
           className={`w-full text-left rounded-xl p-4 transition-all duration-300 ${
  activePage === "goals"
    ? "bg-gradient-to-r from-purple-600 to-indigo-600 shadow-lg scale-105"
    : "bg-zinc-800 hover:bg-zinc-700 hover:scale-105"
}`}
        >
            🎯 Goals ({dashboard.goals})
          </button>

         <button
            onClick={() => setActivePage("analytics")}
            className={`w-full text-left rounded-xl p-4 transition-all duration-300 ${
  activePage === "analytics"
    ? "bg-gradient-to-r from-purple-600 to-indigo-600 shadow-lg scale-105"
    : "bg-zinc-800 hover:bg-zinc-700 hover:scale-105"
}`}
         >
            📊 Analytics
          </button>

          <button
              onClick={() => setActivePage("settings")}
              className={`w-full text-left rounded-xl p-4 transition-all duration-300 ${
  activePage === "settings"
    ? "bg-gradient-to-r from-purple-600 to-indigo-600 shadow-lg scale-105"
    : "bg-zinc-800 hover:bg-zinc-700 hover:scale-105"
}`}
          >
              ⚙️ Settings
            </button>

        </div>

        <div className="mt-10 border-t border-zinc-800 pt-6 text-center">

    <p className="text-zinc-400 font-semibold">
        NOVA Life OS
    </p>

    <p className="text-zinc-500 text-sm mt-1">
        Version 1.0
    </p>

    <p className="text-zinc-600 text-xs mt-3">
        Built with ❤️ using
        <br />
        React • Flask • Gemini
    </p>

</div>

      </div>

      {/* Main */}

      <div className="flex-1 flex flex-col h-screen overflow-hidden">

        <div className="border-b border-zinc-800 p-5 bg-zinc-900/40 backdrop-blur-lg">

          <h2 className="text-3xl font-bold">
            Welcome back 👋
          </h2>

          <p className="text-zinc-400 mt-1">
            NOVA — Your AI Life Operating System
          </p>

          <p className="text-zinc-500 mt-1">
            Organize • Plan • Think • Build
          </p>

        </div>

        <div className="flex-1 p-8 flex flex-col overflow-hidden">


          <div className="grid grid-cols-4 gap-5 mb-8">

  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 hover:border-purple-500 hover:-translate-y-1 transition-all duration-300">
    <p className="text-2xl">📌</p>
    <p className="text-zinc-400">Tasks</p>
    <h3 className="text-2xl font-bold mt-2">{dashboard.tasks}</h3>
  </div>

  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 hover:border-purple-500 hover:-translate-y-1 transition-all duration-300">
    <p className="text-2xl">📝</p>
    <p className="text-zinc-400">Notes</p>
    <h3 className="text-2xl font-bold mt-2">{dashboard.notes}</h3>
  </div>

  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 hover:border-purple-500 hover:-translate-y-1 transition-all duration-300">
    <p className="text-2xl">📅</p>
    <p className="text-zinc-400">Events</p>
    <h3 className="text-2xl font-bold mt-2">{dashboard.events}</h3>
  </div>

  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 hover:border-purple-500 hover:-translate-y-1 transition-all duration-300">
    <p className="text-2xl">🎯</p>
    <h3 className="text-2xl font-bold mt-2">{dashboard.goals}</h3>
    <p className="text-zinc-400">Goals</p>
  </div>

</div>

    {activePage === "tasks" && (
  <div className="flex-1 bg-zinc-900 rounded-3xl border border-zinc-800 p-8 overflow-y-auto">

    <div className="mb-8">

  <div className="text-5xl">
    📌
  </div>

  <h2 className="text-3xl font-bold mt-3">
    My Tasks
  </h2>

  <p className="text-zinc-400 mt-2">
    Manage everything you need to finish today.
  </p>

</div>

    {tasks.length === 0 ? (
      <p className="text-zinc-400">No tasks yet.</p>
    ) : (
      tasks.map((task) => (
        <div
  key={task.id}
  className="bg-zinc-800 border-l-4 border-purple-500 rounded-xl p-5 mb-4 hover:scale-[1.02] hover:bg-zinc-700 transition-all duration-300 shadow-md"
>
  <p className="text-lg">{task.task}</p>
</div>
      ))
    )}

  </div>
)}

{activePage === "notes" && (
  <div className="flex-1 bg-zinc-900 rounded-3xl border border-zinc-800 p-8 overflow-y-auto">

    <div className="mb-8">

  <div className="text-5xl">
    📝
  </div>

  <h2 className="text-3xl font-bold mt-3">
    My Notes
  </h2>

  <p className="text-zinc-400 mt-2">
    Everything you want NOVA to remember.
  </p>

</div>

    {notes.length === 0 ? (
      <p className="text-zinc-400">No notes yet.</p>
    ) : (
      notes.map((note) => (
        <div
  key={note.id}
  className="bg-zinc-800 border-l-4 border-blue-500 rounded-xl p-5 mb-4 hover:scale-[1.02] hover:bg-zinc-700 transition-all duration-300 shadow-md"
>
  <p className="text-lg">{note.note}</p>
</div>
      ))
    )}

  </div>
)}

{activePage === "events" && (
  <div className="flex-1 bg-zinc-900 rounded-3xl border border-zinc-800 p-8 overflow-y-auto">

    <div className="mb-8">

  <div className="text-5xl">
    📝
  </div>

  <h2 className="text-3xl font-bold mt-3">
    My Events
  </h2>

  <p className="text-zinc-400 mt-2">
    Upcoming meetings and reminders.
  </p>

</div>

    {events.length === 0 ? (
      <p className="text-zinc-400">No events yet.</p>
    ) : (
      events.map((event) => (
        <div
  key={event.id}
  className="bg-zinc-800 border-l-4 border-green-500 rounded-xl p-5 mb-4 hover:scale-[1.02] hover:bg-zinc-700 transition-all duration-300 shadow-md"
>
  <p className="text-lg">{event.event}</p>
</div>
      ))
    )}

  </div>
)}

{activePage === "goals" && (
  <div className="flex-1 bg-zinc-900 rounded-3xl border border-zinc-800 p-8 overflow-y-auto">

   <div className="mb-8">

  <div className="text-5xl">
    📝
  </div>

  <h2 className="text-3xl font-bold mt-3">
    My Goals
  </h2>

  <p className="text-zinc-400 mt-2">
    Track your long-term ambitions.
  </p>

</div>

    {goals.length === 0 ? (
      <p className="text-zinc-400">No goals yet.</p>
    ) : (
      goals.map((goal) => (
        <div
  key={goal.id}
  className="bg-zinc-800 border-l-4 border-yellow-500 rounded-xl p-5 mb-4 hover:scale-[1.02] hover:bg-zinc-700 transition-all duration-300 shadow-md"
>
  <p className="text-lg">{goal.goal}</p>
</div>
      ))
    )}

  </div>
)}

{activePage === "analytics" && (
  <div className="flex-1 bg-zinc-900 rounded-3xl border border-zinc-800 p-8 overflow-y-auto">

    <h2 className="text-3xl font-bold mb-8">
      📊 Analytics Dashboard
    </h2>
    <p className="text-zinc-400 mt-2 mb-8">
      Track your productivity and monitor your progress with NOVA.
    </p>

    <div className="grid grid-cols-2 gap-6">

      <div className="bg-zinc-800 rounded-2xl p-6 hover:scale-105 hover:border-purple-500 border border-transparent transition-all duration-300 shadow-lg">
        <h3 className="text-xl font-semibold">📌 Tasks</h3>
        <p className="text-5xl font-bold mt-4">{dashboard.tasks}</p>
      </div>

      <div className="bg-zinc-800 rounded-2xl p-6 hover:scale-105 hover:border-purple-500 border border-transparent transition-all duration-300 shadow-lg">
        <h3 className="text-xl font-semibold">📝 Notes</h3>
        <p className="text-5xl font-bold mt-4">{dashboard.notes}</p>
      </div>

      <div className="bg-zinc-800 rounded-2xl p-6 hover:scale-105 hover:border-purple-500 border border-transparent transition-all duration-300 shadow-lg">
        <h3 className="text-xl font-semibold">📅 Events</h3>
        <p className="text-5xl font-bold mt-4">{dashboard.events}</p>
      </div>

      <div className="bg-zinc-800 rounded-2xl p-6 hover:scale-105 hover:border-purple-500 border border-transparent transition-all duration-300 shadow-lg">
        <h3 className="text-xl font-semibold">🎯 Goals</h3>
        <p className="text-5xl font-bold mt-4">{dashboard.goals}</p>
      </div>

    </div>

    <div className="mt-10 bg-zinc-800 rounded-2xl p-6">
      <h3 className="text-2xl font-bold">
        Productivity Score
      </h3>

      <div className="mt-8 bg-gradient-to-r from-purple-700 to-indigo-700 rounded-2xl p-6">

      <h3 className="text-2xl font-bold">
        🤖 NOVA Insights
      </h3>

      <ul className="mt-4 space-y-3 text-lg">
        <li>📌 You currently have <b>{dashboard.tasks}</b> active tasks.</li>
        <li>📝 You've saved <b>{dashboard.notes}</b> notes.</li>
        <li>📅 You have <b>{dashboard.events}</b> upcoming events.</li>
        <li>🎯 You are tracking <b>{dashboard.goals}</b> goals.</li>
      </ul>

    </div>

      <p className="text-6xl font-bold text-purple-500 mt-4">
        {dashboard.tasks + dashboard.notes + dashboard.events + dashboard.goals}
      </p>

      <p className="text-zinc-400 mt-2">
        Overall productivity based on Tasks, Notes, Events and Goals.
      </p>
    </div>

  </div>
)}

{activePage === "settings" && (
  <div className="flex-1 bg-zinc-900 rounded-3xl border border-zinc-800 p-8 overflow-y-auto">

    <h2 className="text-3xl font-bold mb-8">
      ⚙️ Settings
    </h2>

    <div className="space-y-5">

      <div className="bg-zinc-800 rounded-2xl p-5">
        <h3 className="text-xl font-semibold">🤖 AI Model</h3>
        <p className="text-zinc-400 mt-2">
          Gemini 2.5 Flash
        </p>
      </div>

      <div className="bg-zinc-800 rounded-2xl p-5">
        <h3 className="text-xl font-semibold">🌙 Theme</h3>
        <p className="text-zinc-400 mt-2">
          Dark Mode Enabled
        </p>
      </div>

      <div className="bg-zinc-800 rounded-2xl p-5">
        <h3 className="text-xl font-semibold">💾 Memory</h3>
        <p className="text-zinc-400 mt-2">
          Local SQLite Database Connected
        </p>
      </div>

      <div className="bg-zinc-800 rounded-2xl p-5">
        <h3 className="text-xl font-semibold">📤 Export Data</h3>

        <button className="mt-4 bg-purple-600 hover:bg-purple-700 px-5 py-2 rounded-xl">
          Feature available in NOVA v2.0
        </button>
      </div>

      <div className="bg-zinc-800 rounded-2xl p-5">
        <h3 className="text-xl font-semibold">🗑 Clear Chat</h3>

        <button
          onClick={() => setMessages([])}
          className="mt-4 bg-red-600 hover:bg-red-700 px-5 py-2 rounded-xl transition-all duration-300"
      >
          Clear Chat
        </button>
      </div>

      <div className="bg-zinc-800 rounded-2xl p-5">
        <h3 className="text-xl font-semibold">ℹ️ Version</h3>
        <p className="text-zinc-400 mt-2">
          NOVA Life OS v1.0
        </p>
      </div>
      <div className="bg-zinc-800 rounded-2xl p-5">

    <h3 className="text-xl font-semibold">
      👨‍💻 Developer
    </h3>

    <p className="text-zinc-400 mt-2">
        ISHA KALRA
    </p>

  </div>

  <div className="text-center mt-10">

    <p className="text-zinc-500">
        NOVA Life OS v1.0
    </p>

    <p className="text-zinc-600 text-sm mt-2">
        Built with ❤️ using React, Flask, Gemini & SQLite
    </p>

</div>

    </div>

  </div>
  
)}

{activePage === "chat" && (

<>
  {/* Chat Box */}

  <div 
    className="h-[65vh] bg-zinc-900 rounded-3xl border border-zinc-800 p-6 overflow-y-auto space-y-6">
    {messages.length === 0 ? (

      <div className="h-full flex flex-col items-center justify-center text-center">

  <div className="text-8xl animate-pulse">
    🌌
  </div>

  <h1 className="text-3xl font-bold text-purple-400 drop-shadow-[0_0_12px_rgba(168,85,247,0.8)]">
    Welcome to NOVA
  </h1>

  <p className="text-zinc-400 mt-4 text-lg">
    Your Personal AI Life Operating System
  </p>

  <div className="mt-10 space-y-3 text-zinc-300">

    <p>💬 Add task Finish React Project</p>

    <p>📝 Remember this note AI Roadmap</p>

    <p>📅 Add event Interview tomorrow at 5 PM</p>

    <p>🎯 My goal is Become AI Engineer</p>

  </div>

</div>

    ) : (

      messages.map((msg, index) => (

        <div
         key={index}
         className={`flex animate-[fadeIn_0.3s_ease] ${
            msg.sender === "You"
              ? "justify-end"
              : "justify-start"
          }`}
        >
        <div ref={chatEndRef}></div>

          <div
           className={`max-w-2xl px-6 py-5 rounded-2xl shadow-lg ${
            msg.sender === "You"
              ? "bg-gradient-to-r from-purple-600 to-indigo-600"
              : "bg-zinc-800 border border-zinc-700"
          }`}
        >

            <p className="text-sm font-semibold mb-1">
              {msg.sender}
            </p>

            <p>{msg.text}</p>
            <p className="text-xs text-zinc-400 mt-3 text-right">
               {msg.time}
            </p>

          </div>

        </div>

      ))

    )}

  {loading && (
  <div className="flex items-center gap-2 px-5 py-4 bg-zinc-800 rounded-2xl w-fit border border-zinc-700">

    <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce"></div>

    <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:0.2s]"></div>

    <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:0.4s]"></div>

    <span className="text-zinc-300 ml-2">
      NOVA is thinking...
    </span>

  </div>
)}

    <div ref={chatEndRef}></div>

  </div>

  {/* Input */}

  <div className="mt-6 flex gap-4">

    <input
      value={message}
      onChange={(e) => setMessage(e.target.value)}
      onKeyDown={(e) => {
        if (e.key === "Enter") sendMessage();
      }}
      placeholder="Message NOVA..."
      className="flex-1 bg-zinc-900 border border-zinc-800 rounded-2xl px-6 py-5 outline-none focus:border-purple-500"
    />

    <div className="flex gap-3">

    <button
      onClick={startListening}
      className={`px-5 rounded-2xl ${
        listening
          ? "bg-red-600"
          : "bg-zinc-800 hover:bg-zinc-700"
      }`}
    >
        🎤
    </button>

    <button
      onClick={sendMessage}
      className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:scale-105 transition-all duration-300 px-8 rounded-2xl shadow-lg"
    >
      Send
    </button>

</div>

  </div>

</>
)}
      </div>
    </div>
  </div>

  );
}

export default App;