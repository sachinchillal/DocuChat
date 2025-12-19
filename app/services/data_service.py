import json
import os
import logging

logger = logging.getLogger(__name__)

def get_data_file_name(meeting_id: int) -> str:
    return f"data/chats_{meeting_id}.json"

def append_user_question_to_chat_history(meeting_id: int, question: str) -> list[dict]:
    # get the chat history
    chat_history = get_chat_history(meeting_id)
    # append the question to the chat history
    # check if the question already exists in the last message
    if len(chat_history) > 0 and chat_history[-1]["role"] == "user":
        chat_history[-1]["parts"][0]["text"] = question
    else:
        chat_history.append({"role": "user", "parts": [{"text": question}]})
        # save the chat history
        save_chat_history(meeting_id, chat_history)
    return chat_history

def append_model_response_to_chat_history(meeting_id: int, response: str) -> list[dict]:
    # get the chat history
    chat_history = get_chat_history(meeting_id)
    # append the response to the chat history
    chat_history.append({"role": "model", "parts": [{"text": response}]})
    # save the chat history
    save_chat_history(meeting_id, chat_history)
    return chat_history
  
def save_chat_history(meeting_id: int, chat_history: list[dict]) -> None:
    # save the chat history to the file
    f = get_data_file_name(meeting_id)
    with open(f, 'w') as file:
        json.dump(chat_history, file)

def get_chat_history(meeting_id: int) -> list[dict]:
    # get the chat history from the file
    f = get_data_file_name(meeting_id)    
    if not os.path.exists(f):
        logger.warning(f"Chat history file not found: {f}")
        return []
    
    with open(f, 'r') as file:
        chat_history = json.load(file)
    return chat_history
