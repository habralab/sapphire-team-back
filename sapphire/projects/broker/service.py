import asyncio
import uuid

from sapphire.common.broker.models.notification import Notification
from sapphire.common.broker.models.projects.participants import (
    ParticipantNotificationData,
    ParticipantNotificationType,
)
from sapphire.common.broker.service import BaseBrokerProducerService
from sapphire.projects.database.models import Participant, ParticipantStatusEnum, Project
from sapphire.projects.settings import ProjectsSettings


class ProjectsBrokerService(BaseBrokerProducerService):
    async def send_participant_requested(self,
        project: Project,
        participant: Participant,
        status: ParticipantStatusEnum
    ) -> None:
        # RECIPIENTS: ONLY OWNER
        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.REQUESTED,
            recipients=[project.owner_id],
            notification_data=await self._create_participant_notification_data(project, participant),
        )

    async def send_participant_joined(self,
        project: Project,
        participant: Participant,
        status: ParticipantStatusEnum,
    ) -> None:
        # RECIPIENTS: PROJECT OWNER AND PARTICIPANTS
        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.JOINED,
            recipients=[project.owner_id] + [p.user_id for p in project.participants],
            notification_data=await self._create_participant_notification_data(project, participant),
        )

    async def send_participant_declined(self,
        project: Project,
        participant: Participant,
        status: ParticipantStatusEnum,
    ) -> None:
        # RECIPIENTS: ONLY OWNER
        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.PARTICIPANT_DECLINED,
            recipients=[project.owner_id],
            notification_data=await self._create_participant_notification_data(project, participant),
        )

    async def send_owner_declined(self,
        project: Project,
        participant: Participant,
        status: ParticipantStatusEnum,
    ) -> None:
        # RECIPIENTS: ONLY PARTICIPANT
        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.OWNER_DECLINED,
            recipients=[participant.user_id],
            notification_data=await self._create_participant_notification_data(project, participant),
        )

    async def send_participant_left(self,
        project: Project,
        participant: Participant,
        status: ParticipantStatusEnum,
    ) -> None:
        # RECIPIENTS: PROJECT OWNER AND PARTICIPANTS
        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.PARTICIPANT_LEFT,
            recipients=[project.owner_id] + [p.user_id for p in project.participants],
            notification_data=await self._create_participant_notification_data(project, participant),
        )

    async def send_owner_exluded(self,
        project: Project,
        participant: Participant,
        status: ParticipantStatusEnum,
    ) -> None:
        # RECIPIENTS: PROJECT OWNER AND PARTICIPANTS
        await self._send_notification_to_recipients(
            notification_type=ParticipantNotificationType.OWNER_EXCLUDED,
            recipients=[project.owner_id] + [p.user_id for p in project.participants],
            notification_data=await self._create_participant_notification_data(project, participant),
        )

    @staticmethod
    async def _send_notification_to_recipients(self,
        notification_type: ParticipantNotificationType,
        recipients: list[uuid.UUID],
        notification_data: ParticipantNotificationData,
        topic: str = "ParticipantNotification"
    ) -> None:
        send_tasks = []
        for recipient_id in recipients:
            notification = Notification(
                type = notification_type,
                data = ParticipantNotificationData.model_validate(participant_notification_data),
                recipient_id = recipient_id,
            )
            send_tasks.append(self.send(
                    topic="ParticipantNotification", message=notification
                )
            )
        await asyncio.gather(*send_tasks)
    
    @staticmethod
    async def _create_participant_notification_data(participant: Participant, project: Project):
        return ParticipantNotificationData(
            user_id=participant.user_id,
            position_id=participant.position_id,
            project_id=project.id
        )

def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: ProjectsSettings,
) -> ProjectsBrokerService:
    return ProjectsBrokerService(
        loop=loop,
        servers=settings.producer_servers,
    )
