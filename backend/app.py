import database
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)

database.initialize_database()
database.init_tasks_table()
database.init_notes_table()
database.init_events_table()
database.init_goals_table()
database.init_memory_table()

import os
print("DATABASE FILE:", os.path.abspath("nova.db"))


@app.route("/")
def home():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Introduce yourself as NOVA, an AI Life Operating System, in exactly 3 short friendly sentences."
    )
    return response.text


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_message = data.get("message", "")
    msg = user_message.lower().strip()

    # Save user message
    database.save_message("user", user_message)

    # =========================
    # ADD TASK
    # =========================
    if msg.startswith("add task") or msg.startswith("create task") or msg.startswith("remind me to"):

        if msg.startswith("add task"):
            task = user_message[8:].replace(":", "").strip()
            
        elif msg.startswith("create task"):
            task = user_message[11:].replace(":", "").strip()
            
        else:
            task = user_message[12:].replace(":", "").strip()
            
        database.add_task(task)

        nova_reply = f"✅ Task added: {task}"

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})

    # =========================
    # SHOW TASKS
    # =========================
    elif (
    "what are my tasks" in msg
    or "what are my task" in msg
    or "show my tasks" in msg
    or "show my task" in msg
    or msg == "tasks"
    or msg == "task"
    or msg == "my tasks"
    or msg == "my task"
):

        tasks = database.get_tasks()

        if not tasks:
            nova_reply = "✅ You have no tasks."
        else:
            task_list = "\n".join(
                [f"{i+1}. {task[1]}" for i, task in enumerate(tasks)]
            )
            nova_reply = f"📌 Your Tasks:\n\n{task_list}"

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    
    # =========================
    # DELETE TASK
    # =========================
    elif (
    msg.startswith("delete task")
    or msg.startswith("remove task")
):

        task = user_message.replace("delete task", "").strip()

        if task.isdigit():

            database.delete_task(int(task))

            nova_reply = f"🗑️ Task {task} deleted."

        else:

            deleted = database.delete_task_by_name(task)

            if deleted:
                nova_reply = f"🗑️ Task '{task}' deleted."
            else:
                nova_reply = "❌ Task not found."

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    # =========================
    # DELETE ALL TASKS
    # =========================
    elif (
        "delete all tasks" in msg
        or "clear all tasks" in msg
    ):

        database.delete_all_tasks()

        nova_reply = "🗑️ All tasks deleted."

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    
    # =========================
    # ADD NOTE
    # =========================
    elif (
        msg.startswith("remember this note")
        or msg.startswith("add note")
        or msg.startswith("save note")
):

        if msg.startswith("remember this note"):
            note = user_message[18:].replace(":", "").strip()

        elif msg.startswith("add note"):
            note = user_message[8:].replace(":", "").strip()
            
        else:
            note = user_message[9:].replace(":", "").strip()
            
        database.add_note(note)

        nova_reply = f"📝 Note saved: {note}"

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})

    # =========================
    # SHOW NOTES
    # =========================
    elif (
    "show my notes" in msg
    or "show my note" in msg
    or "show notes" in msg
    or "show note" in msg
    or msg == "notes"
    or msg == "note"
):

        notes = database.get_notes()

        if not notes:
            nova_reply = "📝 You have no notes."

        else:
            note_list = "\n".join(
                [f"{i+1}. {note[1]}" for i, note in enumerate(notes)]
            )

            nova_reply = f"📝 Your Notes:\n\n{note_list}"

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    # =========================
    # DELETE NOTE
    # =========================
    elif (
    msg.startswith("delete note")
    or msg.startswith("remove note")
):

        note = user_message.replace("delete note", "").strip()

        if note.isdigit():

            database.delete_note(int(note))
        
            nova_reply = f"🗑️ Note {note} deleted."

        else:

            deleted = database.delete_note_by_name(note)

            if deleted:
                nova_reply = f"🗑️ Note '{note}' deleted."
            else:
                nova_reply = "❌ Note not found."

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})

    # =========================
    # DELETE ALL NOTES
    # =========================
    elif (
        "delete all notes" in msg
        or "clear all notes" in msg
    ):

        database.delete_all_notes()

        nova_reply = "🗑️ All notes deleted."

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    # =========================
    # ADD EVENT
    # =========================
    elif (
        msg.startswith("add event")
        or msg.startswith("schedule")
        or msg.startswith("create event")
):

        if msg.startswith("add event"):
            event = user_message[9:].replace(":", "").strip()

        elif msg.startswith("schedule"):
            event = user_message[8:].replace(":", "").strip()
            
        else:
            event = user_message[12:].replace(":", "").strip()
            
        database.add_event(event)

        nova_reply = f"📅 Event scheduled: {event}"

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    # =========================
    # DELETE EVENT
    # =========================
    elif (
    msg.startswith("delete event")
    or msg.startswith("remove event")
):

        event = user_message.replace("delete event", "").strip()

        if event.isdigit():

            database.delete_event(int(event))

            nova_reply = f"🗑️ Event {event} deleted."

        else:

            deleted = database.delete_event_by_name(event)

            if deleted:
                nova_reply = f"🗑️ Event '{event}' deleted."
            else:
                nova_reply = "❌ Event not found."

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    # =========================
    # DELETE ALL EVENTS
    # =========================
    elif (
        "delete all events" in msg
        or "clear all events" in msg
    ):

        database.delete_all_events()

        nova_reply = "🗑️ All events deleted."

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})

    # =========================
    # SHOW EVENTS
    # =========================
    elif (
    "calendar" in msg
    or "events" in msg
    or "event" in msg
    or "show events" in msg
    or "show event" in msg
):
        events = database.get_events()

        if not events:
            nova_reply = "📅 No upcoming events."

        else:
            event_list = "\n".join(
                [f"{i+1}. {e[1]}" for i, e in enumerate(events)]
            )

            nova_reply = f"📅 Your Events:\n\n{event_list}"

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
   # =========================
    # ADD GOAL
    # =========================
    elif (
        msg.startswith("add goal")
        or msg.startswith("my goal is")
):

        if msg.startswith("add goal"):
            goal = user_message[8:].replace(":", "").strip()

        else:
            goal = user_message[10:].replace(":", "").strip()

        database.add_goal(goal)

        nova_reply = f"🎯 Goal added: {goal}"

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    # =========================
    # DELETE GOAL
    # =========================
    elif (
    msg.startswith("delete goal")
    or msg.startswith("remove goal")
):

        goal = user_message.replace("delete goal", "").strip()

        if goal.isdigit():

            database.delete_goal(int(goal))

            nova_reply = f"🗑️ Goal {goal} deleted."

        else:

            deleted = database.delete_goal_by_name(goal)

            if deleted:
                nova_reply = f"🗑️ Goal '{goal}' deleted."
            else:
                nova_reply = "❌ Goal not found."

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    
    # =========================
    # DELETE ALL GOALS
    # =========================
    elif msg == "delete all goals":

        database.delete_all_goals()

        nova_reply = "🗑️ All goals deleted."

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    

    # =========================
    # SHOW GOALS
    # =========================
    elif (
    "show goals" in msg
    or "show goal" in msg
    or msg == "goals"
    or msg == "goal"
):

        goals = database.get_goals()

        if not goals:
            nova_reply = "🎯 You have no goals."

        else:
            goal_list = "\n".join(
            [f"{i+1}. {g[1]}" for i, g in enumerate(goals)]
)

            nova_reply = f"🎯 Your Goals:\n\n{goal_list}"

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})

    
    # =========================
    # SAVE NAME
    # =========================
    elif msg.startswith("my name is"):

        try:
            name = user_message[user_message.lower().find("my name is") + len("my name is"):].strip()

            database.save_memory("name", name)

            nova_reply = f"😊 Nice to meet you, {name}! I'll remember your name."

        except Exception as e:
            nova_reply = f"ERROR: {e}"

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    # =========================
    # RECALL NAME
    # =========================
    elif "what's my name" in msg or "what is my name" in msg:

        name = database.get_memory("name")

        if name:
            nova_reply = f"😊 Your name is {name}."
        else:
            nova_reply = "I don't know your name yet."

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    
    # =========================
    # GENERIC MEMORY
    # =========================
    elif msg.startswith("remember that"):

        try:
            text = user_message[user_message.lower().find("remember that") + len("remember that"):].strip()

            if " is " in text:
               key, value = text.split(" is ", 1)

               key = key.strip().lower()

               # Remove leading "my "
            if key.startswith("my "):
                key = key[3:]

                value = value.strip()

                database.save_memory(key, value)

                nova_reply = f"🧠 I'll remember your {key}."
            else:
                nova_reply = "Please use: Remember that <something> is <value>"

        except Exception as e:
            nova_reply = f"ERROR: {e}"

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    
    # =========================
    # RECALL MEMORY
    # =========================
    elif msg.startswith("what is my"):

        key = (
        user_message.lower()
        .replace("what is my", "")
        .replace("?", "")
        .strip()
)
        value = database.get_memory(key)

        if value:
            nova_reply = f"🧠 Your {key} is {value}."
        else:
            nova_reply = f"I don't know your {key} yet."

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})
    
    # =========================
    # PLAN MY DAY
    # =========================
    elif "plan my day" in msg:

        tasks = database.get_tasks()
        events = database.get_events()
        goals = database.get_goals()

        reply = "🗓 Your AI Daily Plan\n\n"

        if tasks:
            reply += "📌 Tasks:\n"
            for t in tasks[:5]:
              reply += f"• {t[1]}\n"

        if events:
            reply += "\n📅 Events:\n"
            for e in events[:5]:
              reply += f"• {e[1]}\n"

        if goals:
            reply += "\n🎯 Goals:\n"
            for g in goals[:3]:
              reply += f"• {g[1]}\n"

        if len(tasks) > 5:   
            reply += "\n⚠️ You have many pending tasks. Try completing a few today."

        elif len(events) > 2:
            reply += "\n📅 You have multiple events scheduled today."

        elif len(goals) > 0:
            reply += "\n🎯 Keep working consistently toward your goals."

        else:
            reply += "\n✨ You have a light schedule today."
        database.save_message("nova", reply)

        return jsonify({"reply": reply})
    
    # =========================
    # GREETING
    # =========================
    elif msg in [
        "hi",
        "hello",
        "hello nova",
        "hey",
        "hey nova",
]:

        nova_reply = "👋 Hello! I'm NOVA, your AI Life Operating System. How can I help you today?"

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})

    # =========================
    # NORMAL AI CHAT
    # =========================
    else:

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
                You are NOVA, an AI Life Operating System.

                You help users with:
                - Tasks
                - Notes
                - Events
                - Goals
                - Daily Planning
                - Productivity

                If the user is chatting casually, answer as NOVA.

                User:
                {user_message}
                """
            )

            nova_reply = response.text

        except Exception:
            nova_reply = "⚠️ Gemini is unavailable right now."

        database.save_message("nova", nova_reply)

        return jsonify({"reply": nova_reply})

@app.route("/dashboard")
def dashboard():

    return jsonify({
        "tasks": database.total_tasks(),
        "notes": database.total_notes(),
        "events": database.total_events(),
        "goals": database.total_goals()
    })
    
        
@app.route("/tasks")
def get_tasks():

    tasks = database.get_tasks()

    return jsonify([
        {
            "id": t[0],
            "task": t[1]
        }
        for t in tasks
    ])


@app.route("/notes")
def get_notes():

    notes = database.get_notes()

    return jsonify([
        {
            "id": n[0],
            "note": n[1]
        }
        for n in notes
    ])


@app.route("/events")
def get_events():

    events = database.get_events()

    return jsonify([
        {
            "id": e[0],
            "event": e[1]
        }
        for e in events
    ])


@app.route("/goals")
def get_goals():

    goals = database.get_goals()

    return jsonify([
        {
            "id": g[0],
            "goal": g[1]
        }
        for g in goals
    ])


if __name__ == "__main__":
    app.run(debug=True)
    
