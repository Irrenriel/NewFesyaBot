ADMIN_REPLY_INFO_TEXT = '''\
<b>Message:</b>
    🆔Message ID: <code>{message_id}</code>
    👤From User:
        ID: <code>{user_id}</code>
        Bot: {user_is_bot}
        First Name: {user_first_name}
        Last Name: {user_last_name}
        Username: {user_username}
        Language Code: <i>{user_language_code}</i>

    📝From Chat:
        ID: <code>{chat_id}</code>
        Type: <i>{chat_type}</i>
        Title: "{chat_title}"
        Username: {chat_username}

    🗓Date: <code>{date}</code>
'''