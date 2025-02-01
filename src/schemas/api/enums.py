from enum import IntEnum, StrEnum


class StatusCode(IntEnum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class Path(StrEnum):
    CONNECT = "/connect"
    STATUS = "/status"
    SEND = "/send"
    CREATE_CHAT = "/create_chat"
    CHAT_GENERATE_INVITE = "/chat_generate_invite"
    CHAT_ACCEPT_INVITE = "/chat_accept_invite"
    UPLOAD_FILE = "/upload_file"
    GET_CHATS = "/get_chats"
    GET_MESSAGES = "/get_messages"
    CREATE_MESSAGE = "/create_message"
    UPDATE_MESSAGE = "/update_message"
    DELETE_MESSAGE = "/delete_message"
    HEALTH_CHECK = "/health_check"
    CREATE_USER = "/create_user"
    GET_USER_ID = "/get_user_id"


class Method(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
