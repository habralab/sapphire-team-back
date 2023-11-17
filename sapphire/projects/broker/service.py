import asyncio
import uuid

from pydantic import BaseModel

from sapphire.common.broker.models.email import Email
from sapphire.common.broker.models.messenger import CreateChat
from sapphire.common.broker.models.notification import Notification
from sapphire.common.broker.models.projects import (
    ParticipantNotificationData,
    ParticipantNotificationType,
)
from sapphire.common.broker.service import BaseBrokerProducerService
from sapphire.projects.database.models import Participant, Project
from sapphire.projects.settings import ProjectsSettings


class ProjectsBrokerService(BaseBrokerProducerService):
    async def send_participant_requested(
        self,
        project: Project,
        participant: Participant
    ) -> None:
        """RECIPIENTS: ONLY OWNER"""
        notification_type = ParticipantNotificationType.REQUESTED

        await self.send(
            topic=self._email_topic,
            message=Email(to=[project.owner_id], type=notification_type),
        )

        await self._send_notification_to_recipients(
            notification_type=notification_type,
            recipients=[project.owner_id],
            notification_data=await self._create_participant_notification_data(
                project, participant
            ),
        )

    async def send_participant_joined(self,
        project: Project,
        participant: Participant,
    ) -> None:
        """RECIPIENTS: PROJECT OWNER AND PARTICIPANTS"""
        notification_type = ParticipantNotificationType.JOINED

        await self.send(
            topic=self._email_topic,
            message=Email(
                to=[project.owner_id] + [p.user_id for p in project.joined_participants],
                type=notification_type,
            ),
        )

        await self._send_notification_to_recipients(
            notification_type=notification_type,
            recipients=[project.owner_id] + [p.user_id for p in project.joined_participants],
            notification_data=await self._create_participant_notification_data(
                project, participant
            ),
        )

    async def send_participant_declined(self,
        project: Project,
        participant: Participant,
    ) -> None:
        """RECIPIENTS: ONLY OWNER"""
        notification_type = ParticipantNotificationType.PARTICIPANT_DECLINED

        await self.send(
            topic=self._email_topic,
            message=Email(to=[project.owner_id], type=notification_type),
        )

        await self._send_notification_to_recipients(
            notification_type=notification_type,
            recipients=[project.owner_id],
            notification_data=await self._create_participant_notification_data(
                project, participant
            ),
        )

    async def send_owner_declined(self,
        project: Project,
        participant: Participant,
    ) -> None:
        """RECIPIENTS: ONLY PARTICIPANT"""
        notification_type = ParticipantNotificationType.OWNER_DECLINED

        await self.send(
            topic=self._email_topic,
            message=Email(
                to=[participant.user_id], type=notification_type
            ),
        )

        await self._send_notification_to_recipients(
            notification_type=notification_type,
            recipients=[participant.user_id],
            notification_data=await self._create_participant_notification_data(
                project, participant
            ),
        )

    async def send_participant_left(self,
        project: Project,
        participant: Participant,
    ) -> None:
        """RECIPIENTS: PROJECT OWNER AND PARTICIPANTS"""
        notification_type = ParticipantNotificationType.PARTICIPANT_LEFT

        await self.send(
            topic=self._email_topic,
            message=Email(
                to=[project.owner_id] + [p.user_id for p in project.joined_participants],
                type=notification_type,
            ),
        )

        await self._send_notification_to_recipients(
            notification_type=notification_type,
            recipients=[project.owner_id] + [p.user_id for p in project.joined_participants],
            notification_data=await self._create_participant_notification_data(
                project, participant
            ),
        )

    async def send_owner_excluded(self,
        project: Project,
        participant: Participant,
    ) -> None:
        """RECIPIENTS: PROJECT OWNER AND PARTICIPANTS"""
        notification_type = ParticipantNotificationType.OWNER_EXCLUDED

        await self.send(
            topic=self._email_topic,
            message=Email(
                to=[project.owner_id] + [p.user_id for p in project.joined_participants],
                type=notification_type,
            ),
        )

        await self._send_notification_to_recipients(
            notification_type=notification_type,
            recipients=[project.owner_id] + [p.user_id for p in project.joined_participants],
            notification_data=await self._create_participant_notification_data(
                project, participant
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

    @staticmethod
    async def _create_participant_notification_data(
         project: Project, participant: Participant,
    ) -> ParticipantNotificationData:
        return ParticipantNotificationData(
            user_id=participant.user_id,
            position_id=participant.position_id,
            project_id=project.id
        )

    async def send_create_chat(
            self,
            is_personal: bool,
            members_ids: list[uuid.UUID]
    ) -> None:
        chat_data = CreateChat(is_personal=is_personal, members_ids=members_ids)
        await self.send(topic="chats", message=chat_data)

    @property
    def _email_topic(self) -> str:
        return "email"

def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: ProjectsSettings,
) -> ProjectsBrokerService:
    return ProjectsBrokerService(
        loop=loop,
        servers=settings.producer_servers,
    )
