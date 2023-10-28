import asyncio
import uuid
from datetime import datetime, timedelta

import backoff
import pytest

from autotests.clients.rest.exceptions import ResponseException
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
        position_id = self.CONTEXT.get("position_id")

        if position_id is not None and project_id is not None:
            event_loop.run_until_complete(oleg_projects_rest_client.remove_project_position(
                project_id=project_id,
                position_id=position_id,
            ))
        if project_id is not None:
            event_loop.run_until_complete(oleg_projects_rest_client.partial_update_project(
                project_id=project_id,
                status=ProjectStatusEnum.FINISHED,
            ))

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_create_project(
            self,
            oleg_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        name = "Oleg Test Project"
        description = "Oleg Test Description"
        deadline = datetime.now() + timedelta(days=90)

        project = await oleg_projects_rest_client.create_project(
            name=name,
            owner_id=oleg_id,
            description=description,
            deadline=deadline,
        )

        self.CONTEXT["project_id"] = project.id

        assert project.name == name
        assert project.description == description
        assert project.owner_id == oleg_id
        assert project.deadline == deadline
        assert project.status == ProjectStatusEnum.PREPARATION

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_project"])
    @pytest.mark.asyncio
    async def test_create_position(self, oleg_projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]

        position = await oleg_projects_rest_client.create_project_position(
            project_id=project_id,
        )

        self.CONTEXT["position_id"] = position.id

        assert position.project_id == project_id
        assert position.is_deleted is False
        assert position.closed_at is None
        
    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_position"])
    @pytest.mark.asyncio
    async def test_create_first_request_to_join_position(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        participant = await matvey_projects_rest_client.create_request_to_join_project_position(
            project_id=project_id,
            position_id=position_id,
        )

        self.CONTEXT["participant_id"] = participant.id

        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.REQUEST

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_first_request_to_join_position"])
    @pytest.mark.asyncio
    async def test_create_duplicate_request_to_join_position(
            self,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        with pytest.raises(ResponseException) as exc_info:
            await matvey_projects_rest_client.create_request_to_join_project_position(
                project_id=project_id,
                position_id=position_id,
            )

        assert exc_info.value.status_code == 400
        assert exc_info.value.body == (
            b'{"detail":"Participant already send request to project or joined in project"}'
        )

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_first_request_to_join_position"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_waiting_notification_about_first_request_to_join_position(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_first_request_to_join_position"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=600)
    async def test_waiting_email_about_first_request_to_join_position(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_first_request_to_join_position"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_chat_opened(self):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_first_request_to_join_position"])
    @pytest.mark.asyncio
    async def test_cancel_first_request_to_join_position(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await matvey_projects_rest_client.update_project_position_participant(
            project_id=project_id,
            position_id=position_id,
            participant_id=participant_id,
            status=ParticipantStatusEnum.DECLINED,
        )

        del self.CONTEXT["participant_id"]

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.DECLINED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_cancel_first_request_to_join_position"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_waiting_notification_about_cancel_first_request_to_join_position(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_cancel_first_request_to_join_position"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=600)
    async def test_waiting_email_about_cancel_first_request_to_join_position(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_cancel_first_request_to_join_position"])
    @pytest.mark.asyncio
    async def test_create_second_request_to_join_position(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        participant = await matvey_projects_rest_client.create_request_to_join_project_position(
            project_id=project_id,
            position_id=position_id,
        )

        self.CONTEXT["participant_id"] = participant.id

        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.REQUEST

    @pytest.mark.dependency(depends=[
        "TestProjectFlow::test_create_second_request_to_join_position",
    ])
    @pytest.mark.asyncio
    async def test_decline_second_request_to_join_position(
            self,
            matvey_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await oleg_projects_rest_client.update_project_position_participant(
            project_id=project_id,
            position_id=position_id,
            participant_id=participant_id,
            status=ParticipantStatusEnum.DECLINED,
        )

        del self.CONTEXT["participant_id"]

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.DECLINED

    @pytest.mark.dependency(depends=[
        "TestProjectFlow::test_decline_second_request_to_join_position",
    ])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_waiting_notification_about_decline_second_request_to_join_position(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=[
        "TestProjectFlow::test_decline_second_request_to_join_position",
    ])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=600)
    async def test_waiting_email_about_decline_second_request_to_join_position(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=[
        "TestProjectFlow::test_decline_second_request_to_join_position",
    ])
    @pytest.mark.asyncio
    async def test_create_third_request_to_join_position(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        participant = await matvey_projects_rest_client.create_request_to_join_project_position(
            project_id=project_id,
            position_id=position_id,
        )

        self.CONTEXT["participant_id"] = participant.id

        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.REQUEST

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_third_request_to_join_position"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_waiting_notification_about_third_request_to_join_position(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_third_request_to_join_position"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=600)
    async def test_waiting_email_about_third_request_to_join_position(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_create_third_request_to_join_position"])
    @pytest.mark.asyncio
    async def test_accept_third_request_to_join_position(
            self,
            matvey_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await oleg_projects_rest_client.update_project_position_participant(
            project_id=project_id,
            position_id=position_id,
            participant_id=participant_id,
            status=ParticipantStatusEnum.JOINED,
        )

        assert participant.id == participant_id
        assert participant.position_id == participant.position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.JOINED

    @pytest.mark.dependency(depends=["TestProjectFlow::test_accept_third_request_to_join_position"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_waiting_notification_about_accept_third_request_to_join_position(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_accept_third_request_to_join_position"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=600)
    async def test_waiting_email_about_accept_third_request_to_join_position(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_accept_third_request_to_join_position"])
    @pytest.mark.asyncio
    async def test_leave_position_by_participant(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await matvey_projects_rest_client.update_project_position_participant(
            project_id=project_id,
            position_id=position_id,
            participant_id=participant_id,
            status=ParticipantStatusEnum.LEFT,
        )

        del self.CONTEXT["participant_id"]

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.LEFT

    @pytest.mark.dependency(depends=["TestProjectFlow::test_leave_position_by_participant"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_waiting_notification_about_leave_position_by_participant(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_leave_position_by_participant"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_waiting_email_about_leave_position_by_participant(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_leave_position_by_participant"])
    @pytest.mark.asyncio
    async def test_create_fourth_request_to_join_position(
            self,
            matvey_id: uuid.UUID,
            matvey_projects_rest_client: ProjectsRestClient,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        participant = await matvey_projects_rest_client.create_request_to_join_project_position(
            project_id=project_id,
            position_id=position_id,
        )

        self.CONTEXT["participant_id"] = participant.id

        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.REQUEST

    @pytest.mark.dependency(depends=[
        "TestProjectFlow::test_create_fourth_request_to_join_position",
    ])
    @pytest.mark.asyncio
    async def test_accept_fourth_request_to_join_position(
            self,
            matvey_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await oleg_projects_rest_client.update_project_position_participant(
            project_id=project_id,
            position_id=position_id,
            participant_id=participant_id,
            status=ParticipantStatusEnum.JOINED,
        )

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.JOINED

    @pytest.mark.dependency(depends=[
        "TestProjectFlow::test_accept_fourth_request_to_join_position",
    ])
    @pytest.mark.asyncio
    async def test_leave_position_by_manager(
            self,
            matvey_id: uuid.UUID,
            oleg_projects_rest_client: ProjectsRestClient,
    ):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]
        participant_id: uuid.UUID = self.CONTEXT["participant_id"]

        participant = await oleg_projects_rest_client.update_project_position_participant(
            project_id=project_id,
            position_id=position_id,
            participant_id=participant_id,
            status=ParticipantStatusEnum.LEFT,
        )

        del self.CONTEXT["participant_id"]

        assert participant.id == participant_id
        assert participant.position_id == position_id
        assert participant.user_id == matvey_id
        assert participant.status == ParticipantStatusEnum.LEFT

    @pytest.mark.dependency(depends=["TestProjectFlow::test_leave_position_by_manager"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=60)
    async def test_waiting_notification_about_leave_position_by_manager(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_leave_position_by_manager"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    @backoff.on_exception(backoff.constant, Exception, max_time=600)
    async def test_waiting_email_about_leave_position_by_manager(
            self,
    ):
        pass

    @pytest.mark.dependency(depends=["TestProjectFlow::test_close_position"])
    @pytest.mark.asyncio
    async def test_move_project_to_work(self, oleg_projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]

        project = await oleg_projects_rest_client.partial_update_project(
            project_id=project_id,
            status=ProjectStatusEnum.IN_WORK,
        )

        assert project.id == project_id
        assert project.status == ProjectStatusEnum.IN_WORK

    @pytest.mark.dependency(depends=["TestProjectFlow::test_leave_position_by_manager"])
    @pytest.mark.asyncio
    async def test_close_position(self, oleg_projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]
        position_id: uuid.UUID = self.CONTEXT["position_id"]

        position = await oleg_projects_rest_client.remove_project_position(
            project_id=project_id,
            position_id=position_id,
        )

        del self.CONTEXT["position_id"]

        assert position.id == position_id
        assert position.project_id == project_id
        assert position.is_deleted is True
        # assert position.closed_at is not None

    @pytest.mark.dependency(depends=["TestProjectFlow::test_close_position"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    async def test_close_project(self, oleg_projects_rest_client: ProjectsRestClient):
        project_id: uuid.UUID = self.CONTEXT["project_id"]

        project = await oleg_projects_rest_client.partial_update_project(
            project_id=project_id,
            status=ProjectStatusEnum.FINISHED,
        )

        del self.CONTEXT["project_id"]

        assert project.id == project_id
        assert project.sttus == ProjectStatusEnum.FINISHED
