import asyncio
import uuid
from typing import Iterable

from pydantic import BaseModel, EmailStr

from collabry.common.broker.models.email import Email, EmailType
from collabry.common.broker.models.messenger import CreateChat
from collabry.common.broker.models.notification import Notification
from collabry.common.broker.models.projects import (
    ParticipantNotificationData,
    ParticipantNotificationType,
)
from collabry.common.broker.service import BaseBrokerProducerService
from collabry.database.models import Participant, Project

from .settings import Settings


class Service(BaseBrokerProducerService):
    async def send_participant_requested(
        self,
        project: Project,
        project_joined_participants: Iterable[Participant],
        participant: Participant,
    ) -> None:
        """RECIPIENTS: ONLY OWNER"""
        await self._send_email(
            recipients=[project.owner.email],
            email_type=EmailType.PARTICIPANT_REQUESTED,
        )

        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.REQUESTED,
            recipients=[project.owner_id],
            notification_data=await self._create_participant_notification_data(
                project=project,
                participant=participant,
            ),
        )

    async def send_participant_joined(
            self,
            project: Project,
            project_joined_participants: Iterable[Participant],
            participant: Participant,
    ) -> None:
        """RECIPIENTS: PARTICIPANTS"""
        await self._send_email(
            recipients=[p.user.email for p in project_joined_participants],
            email_type=EmailType.PARTICIPANT_JOINED,
        )

        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.JOINED,
            recipients=[p.user_id for p in project_joined_participants],
            notification_data=await self._create_participant_notification_data(
                project=project,
                participant=participant,
            ),
        )

    async def send_participant_declined(
            self,
            project: Project,
            project_joined_participants: Iterable[Participant],
            participant: Participant,
    ) -> None:
        """RECIPIENTS: ONLY OWNER"""
        await self._send_email(
            recipients=[project.owner.email], email_type=EmailType.PARTICIPANT_DECLINED
        )

        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.PARTICIPANT_DECLINED,
            recipients=[project.owner_id],
            notification_data=await self._create_participant_notification_data(
                project=project,
                participant=participant,
            ),
        )

    async def send_owner_declined(
            self,
            project: Project,
            project_joined_participants: Iterable[Participant],
            participant: Participant,
    ) -> None:
        """RECIPIENTS: ONLY PARTICIPANT"""
        await self._send_email(
            recipients=[participant.user.email], email_type=EmailType.OWNER_DECLINED
        )

        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.OWNER_DECLINED,
            recipients=[participant.user_id],
            notification_data=await self._create_participant_notification_data(
                project=project,
                participant=participant,
            ),
        )

    async def send_participant_left(
            self,
            project: Project,
            project_joined_participants: Iterable[Participant],
            participant: Participant,
    ) -> None:
        """RECIPIENTS: PROJECT OWNER AND PARTICIPANTS"""
        await self._send_email(
            recipients=[project.owner.email] + [p.user.email for p in project_joined_participants],
            email_type=EmailType.PARTICIPANT_LEFT,
        )

        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.PARTICIPANT_LEFT,
            recipients=[project.owner_id] + [p.user_id for p in project_joined_participants],
            notification_data=await self._create_participant_notification_data(
                project=project,
                participant=participant,
            ),
        )

    async def send_owner_excluded(
            self,
            project: Project,
            project_joined_participants: Iterable[Participant],
            participant: Participant,
    ) -> None:
        """RECIPIENTS: PROJECT OWNER AND PARTICIPANTS"""
        await self._send_email(
            recipients=[project.owner.email] + [p.user.email for p in project_joined_participants],
            email_type=EmailType.OWNER_EXCLUDED,
        )

        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.OWNER_EXCLUDED,
            recipients=[project.owner_id] + [p.user_id for p in project_joined_participants],
            notification_data=await self._create_participant_notification_data(
                project=project,
                participant=participant,
            ),
        )

    async def _send_notification_to_recipients(self,
        notification_type: ParticipantNotificationType,
        recipients: list[uuid.UUID],
        notification_data: BaseModel,
        topic: str = "notifications",
    ) -> None:
        send_tasks = []
        for recipient_id in recipients:
            notification = Notification(
                type=notification_type,
                data=notification_data.model_dump(),
                recipient_id=recipient_id,
            )
            send_tasks.append(self.send(topic=topic, message=notification))
        await asyncio.gather(*send_tasks)

    async def _send_email(
        self, recipients: list[EmailStr], email_type: EmailType, topic: str = "email"
    ):
        await self.send(topic=topic, message=Email(to=recipients, type=email_type))

    @staticmethod
    async def _create_participant_notification_data(
        project: Project,
        participant: Participant,
    ) -> ParticipantNotificationData:
        return ParticipantNotificationData(
            project_id=project.id,
            project_name=project.name,
            position_id=participant.position_id,
            participant_id=participant.user_id,
            owner_id=project.owner_id,
        )

    async def send_create_chat(
            self,
            is_personal: bool,
            members_ids: list[uuid.UUID]
    ) -> None:
        chat_data = CreateChat(is_personal=is_personal, members_ids=members_ids)
        await self.send(topic="chats", message=chat_data)


def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: Settings,
) -> Service:
    return Service(loop=loop, servers=settings.servers)
