import asyncio
import io
import uuid
from datetime import datetime, timedelta, timezone
from http import HTTPStatus

import backoff
import pytest
from faker import Faker

from autotests.clients.email import EmailClient
from autotests.clients.rest.exceptions import ResponseException
from autotests.clients.rest.messenger.client import MessengerRestClient
from autotests.clients.rest.projects.client import ProjectsRestClient
from autotests.clients.rest.projects.enums import ParticipantStatusEnum, ProjectStatusEnum


class TestProjectFlow:
    CONTEXT = {}

    @pytest.fixture(autouse=True, scope="class")
    def cleanup(
            self,
            event_loop: asyncio.AbstractEventLoop,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        project_id = self.CONTEXT.get("project_id")

        if project_id is not None:
            try:
                event_loop.run_until_complete(oleg_projects_rest_client.partial_update_project(
                    project_id=project_id,
                    status=ProjectStatusEnum.FINISHED,
                ))
            except ResponseException:
                pass

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_create_project(
            self,
            faker: Faker,
            oleg_id: uuid.UUID,
            oleg_activated_projects_rest_client: ProjectsRestClient,
    ):
        name = faker.job() + " Сервис"
        description = faker.text()
        startline = datetime.now(tz=timezone.utc) + timedelta(days=30)
        deadline = datetime.now(tz=timezone.utc) + timedelta(days=90)

        project = await oleg_activated_projects_rest_client.create_project(
            owner_id=oleg_id,
            name=name,
            description=description,
            deadline=deadline,
            startline=startline,
        )

        self.CONTEXT["project_id"] = project.id
        self.CONTEXT["project_name"] = name
        self.CONTEXT["project_description"] = description
        self.CONTEXT["project_deadline"] = deadline

        assert project.name == name
        assert project.description == description
        assert project.owner_id == oleg_id
        assert project.deadline == deadline
        assert project.status == ProjectStatusEnum.PREPARATION

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_project"])
    @pytest.mark.asyncio
    async def test_get_project(self, projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        project_name: str = self.CONTEXT["project_name"]
        project_description: str = self.CONTEXT["project_description"]
        project_deadline: datetime = self.CONTEXT["project_deadline"]

        project = await projects_rest_client.get_project(project_id=project_id)

        assert project.id == project_id
        assert project.name == project_name
        assert project.description == project_description
        assert project.deadline == project_deadline
        assert project.status == ProjectStatusEnum.PREPARATION

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_project"])
    @pytest.mark.asyncio
    async def test_finish_project_from_preparation(self, oleg_projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        project = await oleg_projects_rest_client.partial_update_project(
            project_id=project_id,
            status=ProjectStatusEnum.FINISHED,
        )
        
        assert project.id == project_id
        assert project.status == ProjectStatusEnum.FINISHED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_finish_project_from_preparation"])
    @pytest.mark.asyncio
    async def test_get_finished_project(self, oleg_projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        project = await oleg_projects_rest_client.get_project(
            project_id=project_id,
        )

        assert project.status == ProjectStatusEnum.FINISHED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_finished_project"])
    @pytest.mark.asyncio
    async def test_return_finished_project_to_preparation(self, oleg_projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        project = await oleg_projects_rest_client.partial_update_project(
            project_id=project_id,
            status=ProjectStatusEnum.PREPARATION,
        )
        
        assert project.id == project_id
        assert project.status == ProjectStatusEnum.PREPARATION

    @pytest.mark.dependency(depends=["TestProjectFlow::test_return_finished_project_to_preparation"])
    @pytest.mark.asyncio
    async def test_create_position(
            self,
            oleg_projects_rest_client: ProjectsRestClient,
            backend_specialization_id: uuid.UUID,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]

        position = await oleg_projects_rest_client.create_position(
            project_id=project_id,
            specialization_id=backend_specialization_id,
        )

        self.CONTEXT["position_id"] = position.id
        self.CONTEXT["position_specialization_id"] = backend_specialization_id

        assert position.project.id == project_id
        assert position.specialization_id == backend_specialization_id
        assert position.closed_at is None

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_position"])
    @pytest.mark.asyncio
    async def test_get_position(self, projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        position_specialization_id: uuid.UUID = self.CONTEXT["position_specialization_id"]

        position = await projects_rest_client.get_position(position_id=position_id)

        assert position.id == position_id
        assert position.project.id == project_id
        assert position.specialization_id == position_specialization_id
        assert position.closed_at is None

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_position"])
    @pytest.mark.asyncio
    async def test_get_positions(self, projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        position_specialization_id: uuid.UUID = self.CONTEXT["position_specialization_id"]

        positions = await projects_rest_client.get_positions(project_id=project_id)

        assert len(positions.data) == 1
        assert positions.data[0].id == position_id
        assert positions.data[0].project.id == project_id
        assert positions.data[0].specialization_id == position_specialization_id
        assert positions.data[0].closed_at is None

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_positions"])
    @pytest.mark.asyncio
    async def test_create_first_request_to_join(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        participant = await matvey_projects_rest_client.create_request_to_join_position(
            position_id=position_id,
        )

        self.CONTEXT["participant_id"] = participant.id

        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.REQUEST

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_first_request_to_join"])
    @pytest.mark.asyncio
    async def test_get_first_request_to_join(
            self,
            matvey_id: uuid.UUID,
            projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await projects_rest_client.get_participant(participant_id=participant_id)

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.REQUEST

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_first_request_to_join"])
    @pytest.mark.asyncio
    async def test_create_duplicate_request_to_join(
            self,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        with pytest.raises(ResponseException) as exc_info:
            await matvey_projects_rest_client.create_request_to_join_position(
                position_id=position_id,
            )

        assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
        assert exc_info.value.body == (
            b'{"detail":"Participant already send request to project or joined in project"}'
        )

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_first_request_to_join"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    async def test_waiting_notification_about_request_to_join(self):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_first_request_to_join"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=600)
    async def test_waiting_email_about_request_to_join(
            self,
            oleg_email_client: EmailClient,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_first_request_to_join"])
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_oleg_chat_opened(
            self,
            oleg_id: uuid.UUID,
            matvey_id: uuid.UUID,
            oleg_messenger_rest_client: MessengerRestClient,
    ):
        chats = await oleg_messenger_rest_client.get_chats(members={oleg_id, matvey_id})

        assert len(chats.data) > 0

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_first_request_participant"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_matvey_chat_opened(
            self,
            matvey_messenger_rest_client: MessengerRestClient,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_first_request_to_join"])
    @pytest.mark.asyncio
    async def test_cancel_first_request_to_join(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await matvey_projects_rest_client.update_participant(
            participant_id=participant_id,
            status=ParticipantStatusEnum.DECLINED,
        )

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.DECLINED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_cancel_first_request_to_join"])
    @pytest.mark.asyncio
    async def test_get_first_cancelled_request_to_join(
            self,
            matvey_id: uuid.UUID,
            projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await projects_rest_client.get_participant(participant_id=participant_id)

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.DECLINED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_first_cancelled_request_to_join"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    async def test_waiting_notification_about_cancel_request_to_join(self):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_first_cancelled_request_to_join"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=600)
    async def test_waiting_email_about_cancel_request_to_join(
            self,
            oleg_email_client: EmailClient,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_first_cancelled_request_to_join"])
    @pytest.mark.asyncio
    async def test_create_second_request_to_join(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        participant = await matvey_projects_rest_client.create_request_to_join_position(
            position_id=position_id,
        )

        self.CONTEXT["participant_id"] = participant.id

        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.REQUEST

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_second_request_to_join"])
    @pytest.mark.asyncio
    async def test_decline_second_request_to_join(
            self,
            matvey_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await oleg_projects_rest_client.update_participant(
            participant_id=participant_id,
            status=ParticipantStatusEnum.DECLINED,
        )

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.DECLINED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_decline_second_request_to_join"])
    @pytest.mark.asyncio
    async def test_get_second_declined_request_to_join(
            self,
            matvey_id: uuid.UUID,
            projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await projects_rest_client.get_participant(participant_id=participant_id)

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.DECLINED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_second_declined_request_to_join"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    async def test_waiting_notification_about_decline_second_request_to_join(self):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_second_declined_request_to_join"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=600)
    async def test_waiting_email_about_decline_second_request_to_join(
            self,
            matvey_email_client: EmailClient,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_second_declined_request_to_join"])
    @pytest.mark.asyncio
    async def test_create_third_request_to_join(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        participant = await matvey_projects_rest_client.create_request_to_join_position(
            position_id=position_id,
        )

        self.CONTEXT["participant_id"] = participant.id

        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.REQUEST

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_third_request_to_join"])
    @pytest.mark.asyncio
    async def test_accept_third_request_to_join(
            self,
            matvey_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await oleg_projects_rest_client.update_participant(
            participant_id=participant_id,
            status=ParticipantStatusEnum.JOINED,
        )

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.JOINED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_accept_third_request_to_join"])
    @pytest.mark.asyncio
    async def test_get_third_accepted_request_to_join(
            self,
            matvey_id: uuid.UUID,
            projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await projects_rest_client.get_participant(participant_id=participant_id)

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.JOINED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_third_accepted_request_to_join"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    async def test_waiting_notification_about_accept_third_request_to_join(self):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_third_accepted_request_to_join"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=600)
    async def test_waiting_email_about_accept_third_request_to_join(
            self,
            matvey_email_client: EmailClient,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_third_accepted_request_to_join"])
    @pytest.mark.asyncio
    async def test_create_owner_request_to_join(
            self,
            oleg_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        participant = await oleg_projects_rest_client.create_request_to_join_position(
            position_id=position_id,
        )

        self.CONTEXT["new_participant_id"] = participant.id

        assert participant.position_id == position_id
        assert participant.user_id == oleg_id
        assert participant.status == ParticipantStatusEnum.REQUEST

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_owner_request_to_join"])
    @pytest.mark.asyncio
    async def test_get_owner_request_to_join(
            self,
            oleg_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["new_participant_id"]

        participant = await oleg_projects_rest_client.get_participant(
            participant_id=participant_id,
        )

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == oleg_id
        assert participant.status == ParticipantStatusEnum.REQUEST

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_owner_request_to_join"])
    @pytest.mark.asyncio
    async def test_owner_accept_request_to_join(
            self,
            oleg_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["new_participant_id"]

        participant = await oleg_projects_rest_client.update_participant(
            participant_id=participant_id,
            status=ParticipantStatusEnum.JOINED,
        )

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == oleg_id
        assert participant.status == ParticipantStatusEnum.JOINED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_owner_accept_request_to_join"])
    @pytest.mark.asyncio
    async def test_get_owner_accepted_request_to_join(
            self,
            oleg_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["new_participant_id"]

        participant = await oleg_projects_rest_client.get_participant(
            participant_id=participant_id,
        )

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == oleg_id
        assert participant.status == ParticipantStatusEnum.JOINED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_owner_accepted_request_to_join"])
    @pytest.mark.asyncio
    async def test_leave_position_by_participant(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await matvey_projects_rest_client.update_participant(
            participant_id=participant_id,
            status=ParticipantStatusEnum.LEFT,
        )

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.LEFT

    @pytest.mark.dependency(depends=["TestProjectFlow::test_leave_position_by_participant"])
    @pytest.mark.asyncio
    async def test_get_third_left_participant(
            self,
            matvey_id: uuid.UUID,
            projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await projects_rest_client.get_participant(participant_id=participant_id)

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.LEFT

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_third_left_participant"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    async def test_waiting_notification_about_leave_position_by_participant(self):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_third_left_participant"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_waiting_email_about_leave_position_by_participant(
            self,
            oleg_email_client: EmailClient,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_third_left_participant"])
    @pytest.mark.asyncio
    async def test_create_fourth_request_to_join(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        participant = await matvey_projects_rest_client.create_request_to_join_position(
            position_id=position_id,
        )

        self.CONTEXT["participant_id"] = participant.id

        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.REQUEST

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_fourth_request_to_join"])
    @pytest.mark.asyncio
    async def test_accept_fourth_request_to_join(
            self,
            matvey_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await oleg_projects_rest_client.update_participant(
            participant_id=participant_id,
            status=ParticipantStatusEnum.JOINED,
        )

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.JOINED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_accept_fourth_request_to_join"])
    @pytest.mark.asyncio
    async def test_leave_position_by_manager(
            self,
            matvey_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await oleg_projects_rest_client.update_participant(
            participant_id=participant_id,
            status=ParticipantStatusEnum.LEFT,
        )

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.LEFT

    @pytest.mark.dependency(depends=["TestProjectFlow::test_leave_position_by_manager"])
    @pytest.mark.asyncio
    async def test_get_fourth_left_participant(
            self,
            matvey_id: uuid.UUID,
            projects_rest_client: ProjectsRestClient,
    ):
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await projects_rest_client.get_participant(participant_id=participant_id)

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.LEFT

    @pytest.mark.dependency(depends=["TestProjectFlow::test_leave_position_by_manager"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    async def test_waiting_notification_about_leave_position_by_manager(self):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_leave_position_by_manager"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=600)
    async def test_waiting_email_about_leave_position_by_manager(
            self,
            matvey_email_client: EmailClient,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_fourth_left_participant"])
    @pytest.mark.asyncio
    async def test_move_project_to_work(self, oleg_projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]

        project = await oleg_projects_rest_client.partial_update_project(
            project_id=project_id,
            status=ProjectStatusEnum.IN_WORK,
        )
        
        assert project.id == project_id
        assert project.status == ProjectStatusEnum.IN_WORK

    @pytest.mark.dependency(depends=["TestProjectFlow::test_move_project_to_work"])
    @pytest.mark.asyncio
    async def test_get_moved_to_work_project(self, projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]

        project = await projects_rest_client.get_project(project_id=project_id)

        assert project.id == project_id
        assert project.status == ProjectStatusEnum.IN_WORK

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_moved_to_work_project"])
    @pytest.mark.asyncio
    async def test_close_position(self, oleg_projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        position = await oleg_projects_rest_client.remove_position(position_id=position_id)

        assert position.id == position_id
        assert position.project.id == project_id
        assert position.closed_at is not None

    @pytest.mark.dependency(depends=["TestProjectFlow::test_close_position"])
    @pytest.mark.asyncio
    async def test_get_closed_position(self, projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        position = await projects_rest_client.get_position(position_id=position_id)

        assert position.id == position_id
        assert position.project.id == project_id
        assert position.closed_at is not None

    @pytest.mark.dependency(depends=["TestProjectFlow::test_get_closed_position"])
    @pytest.mark.asyncio
    async def test_close_project(self, oleg_projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]

        project = await oleg_projects_rest_client.partial_update_project(
            project_id=project_id,
            status=ProjectStatusEnum.FINISHED,
        )

        assert project.id == project_id
        assert project.status == ProjectStatusEnum.FINISHED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_close_project"])
    @pytest.mark.asyncio
    async def test_get_closed_project(self, projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]

        project = await projects_rest_client.get_project(
            project_id=project_id,
        )

        assert project.id == project_id
        assert project.status == ProjectStatusEnum.FINISHED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_close_project"])
    @pytest.mark.asyncio
    async def test_create_review(
        self,
        faker: Faker,
        oleg_id: uuid.UUID,
        matvey_id: uuid.UUID, 
        oleg_projects_rest_client: ProjectsRestClient
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        review_rate = faker.pyint(1, 5)
        review_text = faker.text()

        review = await oleg_projects_rest_client.create_review(
            project_id=project_id,
            user_id=matvey_id,
            rate=review_rate,
            text=review_text,
        )

        self.CONTEXT["review_text"] = review_text

        assert review.project_id == project_id
        assert review.from_user_id == oleg_id
        assert review.to_user_id == matvey_id
        assert review.rate == review_rate
        assert review.text == review_text

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_review"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    async def test_get_review(self):
        project_id: uuid.UUID = self.CONTEXT["project_id"]


class TestProjectAvatarFlow:
    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_upload_project_avatar(
            self,
            avatar_file: io.BytesIO,
            oleg_projects_rest_client: ProjectsRestClient,
            project_id: uuid.UUID,
    ):
        project = await oleg_projects_rest_client.upload_project_avatar(
            project_id=project_id,
            avatar=avatar_file,
        )

        assert project.id == project_id

    @pytest.mark.dependency(depends=["TestProjectAvatarFlow::test_upload_project_avatar"])
    @pytest.mark.asyncio
    async def test_get_project_avatar(
            self,
            avatar_file: io.BytesIO,
            oleg_projects_rest_client: ProjectsRestClient,
            project_id: uuid.UUID,
    ):
        avatar = await oleg_projects_rest_client.get_project_avatar(project_id=project_id)

        assert avatar.read() == avatar_file.read()

    @pytest.mark.dependency(depends=["TestProjectAvatarFlow::test_get_project_avatar"])
    @pytest.mark.asyncio
    async def test_remove_project_avatar(
            self,
            oleg_projects_rest_client: ProjectsRestClient,
            project_id: uuid.UUID,
    ):
        project = await oleg_projects_rest_client.remove_project_avatar(project_id=project_id)

        assert project.id == project_id

    @pytest.mark.dependency(depends=["TestProjectAvatarFlow::test_remove_project_avatar"])
    @pytest.mark.asyncio
    async def test_get_project_avatar_after_removing(
            self,
            project_id: uuid.UUID,
            projects_rest_client: ProjectsRestClient,
    ):
        avatar = await projects_rest_client.get_project_avatar(project_id=project_id)

        assert avatar.read() == b"null"


class TestPositionSkillsFlow:
    CONTEXT = {}

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_update_position_skills(
            self,
            oleg_projects_rest_client: ProjectsRestClient,
            position_id: uuid.UUID,
            git_skill_id: uuid.UUID,
            javascript_skill_id: uuid.UUID,
    ):
        new_skills = {git_skill_id, javascript_skill_id}

        skills = await oleg_projects_rest_client.update_position_skills(
            position_id=position_id,
            skills=new_skills,
        )

        self.CONTEXT["skills"] = new_skills

        assert skills == new_skills

    @pytest.mark.dependency(depends=["TestPositionSkillsFlow::test_update_position_skills"])
    @pytest.mark.asyncio
    async def test_get_position_skills(
            self,
            projects_rest_client: ProjectsRestClient,
            position_id: uuid.UUID,
    ):
        position_skills: set[uuid.UUID] = self.CONTEXT["skills"]

        skills = await projects_rest_client.get_position_skills(position_id=position_id)

        assert skills == position_skills

    @pytest.mark.dependency(depends=["TestPositionSkillsFlow::test_get_position_skills"])
    @pytest.mark.asyncio
    async def test_add_new_position_skills(
            self,
            oleg_projects_rest_client: ProjectsRestClient,
            position_id: uuid.UUID,
            python_skill_id: uuid.UUID,
            uiux_design_skill_id: uuid.UUID,
    ):
        position_skills: set[uuid.UUID] = self.CONTEXT["skills"]
        position_skills |= {python_skill_id, uiux_design_skill_id}

        skills = await oleg_projects_rest_client.update_position_skills(
            position_id=position_id,
            skills=position_skills,
        )

        self.CONTEXT["skills"] = position_skills

        assert skills == position_skills

    @pytest.mark.dependency(depends=["TestPositionSkillsFlow::test_add_new_position_skills"])
    @pytest.mark.asyncio
    async def test_get_new_position_skills(
            self,
            projects_rest_client: ProjectsRestClient,
            position_id: uuid.UUID,
    ):
        position_skills: set[uuid.UUID] = self.CONTEXT["skills"]

        skills = await projects_rest_client.get_position_skills(position_id=position_id)

        assert skills == position_skills

    @pytest.mark.dependency(depends=["TestPositionSkillsFlow::test_get_new_position_skills"])
    @pytest.mark.asyncio
    async def test_empty_position_skills(
            self,
            oleg_projects_rest_client: ProjectsRestClient,
            position_id: uuid.UUID,
    ):
        position_skills = set()

        skills = await oleg_projects_rest_client.update_position_skills(
            position_id=position_id,
            skills=position_skills,
        )

        self.CONTEXT["skills"] = position_skills

        assert skills == position_skills

    @pytest.mark.dependency(depends=["TestPositionSkillsFlow::test_empty_position_skills"])
    @pytest.mark.asyncio
    async def test_get_empty_position_skills(
            self,
            projects_rest_client: ProjectsRestClient,
            position_id: uuid.UUID,
    ):
        position_skills: set[uuid.UUID] = self.CONTEXT["skills"]

        skills = await projects_rest_client.get_position_skills(position_id=position_id)

        assert skills == position_skills
