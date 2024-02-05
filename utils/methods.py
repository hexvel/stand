from dataclasses import dataclass

from vkbottle.user import Message


@dataclass
class APIMethod:
    message: Message = object
    success: bool = False
    data: dict = dict

    async def edit_messages(
        self, text: str = None, message_id: int = None, attachments: str = None
    ) -> None:
        """Edit message.

        Returns:
            NoneType: None
        """

        if message_id is None:
            message_id = self.message.id

        try:
            await self.message.ctx_api.messages.edit(
                peer_id=self.message.peer_id,
                message_id=message_id,
                keep_forward_messages=True,
                message=text,
                attachment=attachments,
            )

            self.success = True
            self.data = text
        except Exception as error:
            await self.message.ctx_api.messages.delete(
                peer_id=self.message.peer_id,
                cmids=self.message.conversation_message_id,
                delete_for_all=True,
            )

            await self.send_messages(text=text, attachments=attachments)
            self.success = False
            self.data = error

    async def send_messages(self, text: str, attachments: str = None) -> None:
        """Send message.

        Returns:
            NoneType: None
        """

        try:
            await self.message.ctx_api.messages.send(
                peer_id=self.message.peer_id,
                message=text,
                random_id=0,
                attachment=attachments,
            )

            self.success = True
            self.data = text
        except Exception as error:
            self.success = False
            self.data = error

    async def delete_messages(self, message_ids: list) -> None:
        """_summary_

        Args:
            message_ids (list): list of ids
        """
        try:
            await self.message.ctx_api.messages.delete(
                peer_id=self.message.peer_id, message_ids=message_ids
            )
        except Exception as error:
            self.success = False
            self.data = error
