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
    async def send_participant_notification(
        self,
        initiator_id: uuid.UUID,
        project: Project,
        participant: Participant,
        status: ParticipantStatusEnum
    ) -> None:
        participant_notification_data = ParticipantNotificationData(
            user_id=participant.user_id,
            position_id=participant.position_id,
            project_id=project.id,
        )

        if status == ParticipantStatusEnum.REQUEST:
            notification_type = ParticipantNotificationType.REQUEST
            recipients = [project.owner_id]

        elif status == ParticipantStatusEnum.JOINED:
            notification_type = ParticipantNotificationType.JOINED
            recipients = [project.owner_id] + [p.user_id for p in project.participants]

        elif status == ParticipantStatusEnum.DECLINED:
            # The Participant withdrew an application
            if initiator_id == participant.user_id:
                notification_type = ParticipantNotificationType.PARTICIPANT_DECLINED
                recipients = [project.owner_id]
            # The Owner declined the participant
            elif initiator_id == project.owner_id:
                notification_type = ParticipantNotificationType.OWNER_DECLINED
                recipients = [participant.user_id]

        elif status == ParticipantStatusEnum.LEFT:
            if initiator_id == participant.user_id:
                notification_type = ParticipantNotificationType.PARTICIPANT_LEFT
                recipients = [project.owner_id] + [p.user_id for p in project.participants]
            elif initiator_id == project.owner_id:
                notification_type = ParticipantNotificationType.OWNER_EXCLUDED
                recipients = [project.owner_id] + [p.user_id for p in project.participants]

        broker_tasks = []
        for recipient_id in recipients:
            notification = Notification(
                type=notification_type,
                data=ParticipantNotificationData.model_validate(participant_notification_data),
                recipient_id=recipient_id,
            )
            broker_tasks.append(self.send(
                    topic="ParticipantNotification", message=notification
                )
            )

        await asyncio.gather(*broker_tasks)


def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: ProjectsSettings,
) -> ProjectsBrokerService:
    return ProjectsBrokerService(
        loop=loop,
        servers=settings.producer_servers,
    )
