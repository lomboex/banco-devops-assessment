from schemas.message import MessageRequest, MessageResponse


class MessageService:
    @staticmethod
    def process_message(data: MessageRequest) -> MessageResponse:
        response_text = f"Hello {data.to} your message will be send"
        return MessageResponse(message=response_text)
