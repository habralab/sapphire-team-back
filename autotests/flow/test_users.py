import io
import uuid

import pytest

from autotests.clients.rest.users.client import UsersRestClient


class TestUserUpdateFlow:
    CONTEXT = {}

    @pytest.fixture(autouse=True, scope="class")
    def cleanup(self, oleg_revert_user_data):
        pass

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_update_user(
            self,
            oleg_id: uuid.UUID,
            oleg_email: str,
            oleg_users_rest_client: UsersRestClient,
    ):
        first_name = "Not-Oleg"
        last_name = "Not-Yurchik"
        about = "New about"
        main_specialization_id = uuid.uuid4()
        secondary_specialization_id = uuid.uuid4()

        user = await oleg_users_rest_client.update_user(
            user_id=oleg_id,
            first_name=first_name,
            last_name=last_name,
            about=about,
            main_specialization_id=main_specialization_id,
            secondary_specialization_id=secondary_specialization_id,
        )

        self.CONTEXT.update({
            "first_name": first_name,
            "last_name": last_name,
            "about": about,
            "main_specialization_id": main_specialization_id,
            "secondary_specialization_id": secondary_specialization_id,
        })

        assert user.id == oleg_id
        assert user.email == oleg_email
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.about == about
        assert user.main_specialization_id == main_specialization_id
        assert user.secondary_specialization_id == secondary_specialization_id

    @pytest.mark.dependency(depends=["TestUserUpdateFlow::test_update_user"])
    @pytest.mark.asyncio
    async def test_get_updated_user(
            self,
            oleg_id: uuid.UUID,
            users_rest_client: UsersRestClient,
    ):
        first_name: str = self.CONTEXT["first_name"]
        last_name: str = self.CONTEXT["last_name"]
        about: str = self.CONTEXT["about"]
        main_specialization_id: uuid.UUID = self.CONTEXT["main_specialization_id"]
        secondary_specialization_id: uuid.UUID = self.CONTEXT["secondary_specialization_id"]

        user = await users_rest_client.get_user(user_id=oleg_id)

        del self.CONTEXT["first_name"]
        del self.CONTEXT["last_name"]
        del self.CONTEXT["about"]
        del self.CONTEXT["main_specialization_id"]
        del self.CONTEXT["secondary_specialization_id"]

        assert user.id == oleg_id
        assert user.email is None
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.about == about
        assert user.main_specialization_id == main_specialization_id
        assert user.secondary_specialization_id == secondary_specialization_id


class TestUserUpdateAvatarFlow:
    @pytest.fixture(autouse=True, scope="class")
    def cleanup(self, oleg_revert_user_avatar):
        pass

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_update_user_avatar(
            self,
            avatar_file: io.BytesIO,
            oleg_id: uuid.UUID,
            oleg_email: str,
            oleg_users_rest_client: UsersRestClient,
    ):
        user = await oleg_users_rest_client.update_user_avatar(user_id=oleg_id, avatar=avatar_file)

        assert user.id == oleg_id
        assert user.email == oleg_email

    @pytest.mark.dependency(depends=["TestUserUpdateAvatarFlow::test_update_user_avatar"])
    @pytest.mark.asyncio
    async def test_get_user_avatar(
            self,
            avatar_file: io.BytesIO,
            oleg_id: uuid.UUID,
            users_rest_client: UsersRestClient,
    ):
        user_avatar = await users_rest_client.get_user_avatar(user_id=oleg_id)

        assert user_avatar.read() == avatar_file.read()


class TestUserUpdateSkillsFlow:
    CONTEXT = {}

    @pytest.fixture(autouse=True, scope="class")
    def cleanup(self, oleg_revert_user_skills):
        pass

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_update_user_skills(
            self,
            oleg_id: uuid.UUID,
            oleg_users_rest_client: UsersRestClient,
    ):
        new_skills = {uuid.uuid4() for _ in range(10)}

        skills = await oleg_users_rest_client.update_user_skills(
            user_id=oleg_id,
            skills=new_skills,
        )

        self.CONTEXT["new_skills"] = new_skills

        assert skills == new_skills

    @pytest.mark.dependency(depends=["TestUserUpdateSkillsFlow::test_update_user_skills"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    async def test_get_user_skills(self, oleg_id: uuid.UUID, users_rest_client: UsersRestClient):
        new_skills: set[uuid.UUID] = self.CONTEXT["new_skills"]

        skills = await users_rest_client.get_user_skills(user_id=oleg_id)

        assert skills == new_skills
