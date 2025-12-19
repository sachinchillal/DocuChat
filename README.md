# DocuChat

This project allows users to chat with documents using the Gemini AI model.

## Setup Instructions

1. Add your Gemini API key to a `.env` file in the root directory:
2. Add meetings transcripts to the `data` folder.
    - Like `data/meeting_1.txt`, `data/meeting_2.txt`, etc.
3. Include the meeting details in `data/meetings.json`:

    ```json
    {
        "id": 1,
        "file": "meeting_1.txt",
        "title": "Project Kickoff",
        "cached_content_name": ""
    }
    ```

## Run the project

```bash
fastapi dev app/main.py
```
