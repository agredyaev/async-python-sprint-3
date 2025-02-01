─────────────────────────────
API Documentation
─────────────────────────────

1. POST /create_chat
   -  Description: Creates a new chat.
   -  Request Body:
      -chat: { name (string), is_private (boolean) }
      -owner: { id (UUID) }
      -members: list of user IDs (UUID)
   -  Response:
      -On success, returns chat details (chat_id, name, etc.)
      -Status Code: 201 (Created)

2. POST /connect
   -  Description: Allows a user to connect to an existing chat.
   -  Request Body:
      -chat: { id (UUID) }
      -user: { id (UUID) }
   -  Response:
      -Returns last messages, unread messages count, and possibly updated "last_seen" timestamp.
      -Status Code: 200 (OK)

3. POST /upload_file
   -  Description: Uploads a file and associates it with a specified chat.
   -  Request Body (UploadRequest extends ChatConnect):
      -file: { name (string), content (bytes) }
      -chat: { id (UUID) }
      -user: { id (UUID) }
   -  Response:
      -Returns file ID and associated chat file ID.
      -Status Code: 200 (OK) or 400 (Bad Request) if file upload fails.

4. POST /chat_generate_invite
   -  Description: Generates an invite link token for a chat.
   -  Request Body:
      -chat: { id (UUID) }
      -inviter: { id (UUID) }
   -  Response:
      -Returns generated token and a formatted invite link.
      -Status Code: 200 (OK)

5. POST /chat_accept_invite
   -  Description: Accepts an invite using a provided token, adding the user to the chat if not already a member.
   -  Request Parameters (can be passed as query parameters or in the body):
      -token: (string)
      -user_id: (UUID)
   -  Response:
      -Returns confirmation with chat ID.
      -Status Code: 200 (OK) or 404/400 for errors.

6. POST /send_message
   -  Description: Posts a new message to the chat as long as the user is a member.
   -  Request Body:
      -content: (string)
      -connect: { chat: { id (UUID) }, user: { id (UUID) } }
   -  Response:
      -Returns confirmation with the message ID.
      -Status Code: 200 (OK)

7. GET /status
   -  Description: Fetches the status of all chats where the user is a member, including unread message counts.
   -  Request Body:
      -{ id (UUID) } (UserId payload)
   -  Response:
      -Returns a list of chats with details and unread_messages_count.
      -Status Code: 200 (OK)

8. POST /create_user
   -  Description: Creates a new user with a unique username.
   -  Request Body:
      -{ username (string) }
   -  Response:
      -Returns the created user's ID and username details.
      -Status Code: 201 (Created)

9. GET /get_user_id
   -  Description: Retrieves the user ID corresponding to the provided username.
   -  Request Body:
      -{ username (string) }
   -  Response:
      -Returns the user ID.
      -Status Code: 200 (OK)

─────────────────────────────
Notes
─────────────────────────────

-  All endpoints exchange data using JSON following the defined request and response models.
-  Standard HTTP status codes (e.g., 200, 201, 400, 404, 500) indicate the result of each operation.
-  Error responses include a "body" with details of the error.
