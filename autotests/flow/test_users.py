import io
import uuid

import pytest
from faker import Faker

from autotests.clients.rest.users.client import UsersRestClient
from autotests.settings import AutotestsSettings


class TestUserAuthFlow:
    CONTEXT = {}

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_signup_user(self, faker: Faker, users_rest_client: UsersRestClient):
        email = f"{uuid.uuid4()}@{faker.domain_name()}"
        password = faker.password(length=16)

        response = await users_rest_client.sign_up(email=email, password=password)

        self.CONTEXT["access_token"] = response.access_token
        self.CONTEXT["user_id"] = response.user.id
        self.CONTEXT["email"] = email
        self.CONTEXT["password"] = password

    @pytest.mark.dependency(depends=["TestUserAuthFlow::test_signup_user"])
    @pytest.mark.asyncio
    async def test_check(self, settings: AutotestsSettings):
        user_id: uuid.UUID = self.CONTEXT["user_id"]
        access_token: str = self.CONTEXT["access_token"]
        users_rest_client = UsersRestClient(
            base_url=str(settings.users_base_url),
            headers={"Authorization": f"Bearer {access_token}"},
        )

        response = await users_rest_client.check_auth()

        assert response.user_id == user_id

    @pytest.mark.dependency(depends=["TestUserAuthFlow::test_signup_user"])
    @pytest.mark.asyncio
    async def test_signin_user(self, users_rest_client: UsersRestClient):
        user_id: uuid.UUID = self.CONTEXT["user_id"]
        email: str = self.CONTEXT["email"]
        password: str = self.CONTEXT["password"]

        response = await users_rest_client.sign_in(email=email, password=password)

        assert response.user.id == user_id
        assert response.user.email == email

    @pytest.mark.dependency(depends=["TestUserAuthFlow::test_signin_user"])
    @pytest.mark.asyncio
    async def test_reset_password_request(self, users_rest_client: UsersRestClient):
        email: str = self.CONTEXT["email"]
        
        await users_rest_client.reset_password_request(email=email)


class TestUserUpdateFlow:
    CONTEXT = {}

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_update_user(
            self,
            oleg_id: uuid.UUID,
            oleg_email: str,
            oleg_users_rest_client: UsersRestClient,
            backend_specialization_id: uuid.UUID,
            web_design_specialization_id: uuid.UUID,
    ):
        first_name = "Not-Oleg"
        last_name = "Not-Yurchik"
        about = "New about"
        telegram = "+79123456789"

        user = await oleg_users_rest_client.update_user(
            user_id=oleg_id,
            first_name=first_name,
            last_name=last_name,
            about=about,
            telegram=telegram,
            main_specialization_id=backend_specialization_id,
            secondary_specialization_id=web_design_specialization_id,
        )

        self.CONTEXT.update({
            "first_name": first_name,
            "last_name": last_name,
            "about": about,
            "telegram": telegram,
            "main_specialization_id": backend_specialization_id,
            "secondary_specialization_id": web_design_specialization_id,
        })

        assert user.id == oleg_id
        assert user.email == oleg_email
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.about == about
        assert user.telegram == telegram
        assert user.main_specialization_id == backend_specialization_id
        assert user.secondary_specialization_id == web_design_specialization_id

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

        assert user.id == oleg_id
        assert user.email is None
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.about == about
        assert user.main_specialization_id == main_specialization_id
        assert user.secondary_specialization_id == secondary_specialization_id


class TestUserAvatarFlow:
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

    @pytest.mark.dependency(depends=["TestUserAvatarFlow::test_update_user_avatar"])
    @pytest.mark.asyncio
    async def test_get_user_avatar(
            self,
            avatar_file: io.BytesIO,
            oleg_id: uuid.UUID,
            users_rest_client: UsersRestClient,
    ):
        user_avatar = await users_rest_client.get_user_avatar(user_id=oleg_id)

        assert user_avatar.read() == avatar_file.read()

    @pytest.mark.dependency(depends=["TestUserAvatarFlow::test_get_user_avatar"])
    @pytest.mark.asyncio
    async def test_remove_user_avatar(
            self,
            oleg_id: uuid.UUID,
            oleg_email: str,
            oleg_users_rest_client: UsersRestClient,
    ):
        user = await oleg_users_rest_client.remove_user_avatar(user_id=oleg_id)

        assert user.id == oleg_id
        assert user.email == oleg_email

    @pytest.mark.dependency(depends=["TestUserAvatarFlow::test_remove_user_avatar"])
    @pytest.mark.asyncio
    async def test_get_user_avatar_after_remove(
            self,
            oleg_id: uuid.UUID,
            users_rest_client: UsersRestClient,
    ):
        avatar = await users_rest_client.get_user_avatar(user_id=oleg_id)

        assert avatar.read() == b"null"


class TestUserSkillsFlow:
    CONTEXT = {}

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_update_user_skills(
            self,
            oleg_id: uuid.UUID,
            oleg_users_rest_client: UsersRestClient,
            python_skill_id: uuid.UUID,
            git_skill_id: uuid.UUID,
    ):
        new_skills = {python_skill_id, git_skill_id}

        skills = await oleg_users_rest_client.update_user_skills(
            user_id=oleg_id,
            skills=new_skills,
        )

        self.CONTEXT["user_skills"] = new_skills

        assert skills == new_skills

    @pytest.mark.dependency(depends=["TestUserSkillsFlow::test_update_user_skills"])
    @pytest.mark.asyncio
    async def test_get_user_skills(self, oleg_id: uuid.UUID, users_rest_client: UsersRestClient):
        user_skills: set[uuid.UUID] = self.CONTEXT["user_skills"]

        skills = await users_rest_client.get_user_skills(user_id=oleg_id)

        assert skills == user_skills

    @pytest.mark.dependency(depends=["TestUserSkillsFlow::test_get_user_skills"])
    @pytest.mark.asyncio
    async def test_add_new_user_skills(
            self,
            oleg_id: uuid.UUID,
            oleg_users_rest_client: UsersRestClient,
            javascript_skill_id: uuid.UUID,
            uiux_design_skill_id: uuid.UUID,
    ):
        user_skills = self.CONTEXT["user_skills"]
        user_skills |= {javascript_skill_id, uiux_design_skill_id}

        skills = await oleg_users_rest_client.update_user_skills(
            user_id=oleg_id,
            skills=user_skills,
        )

        self.CONTEXT["user_skills"] = user_skills

        assert skills == user_skills

    @pytest.mark.dependency(depends=["TestUserSkillsFlow::test_add_new_user_skills"])
    @pytest.mark.asyncio
    async def test_get_new_user_skills(
            self,
            oleg_id: uuid.UUID,
            users_rest_client: UsersRestClient,
    ):
        user_skills: set[uuid.UUID] = self.CONTEXT["user_skills"]

        skills = await users_rest_client.get_user_skills(user_id=oleg_id)

        assert skills == user_skills

    @pytest.mark.dependency(depends=["TestUserSkillsFlow::test_get_new_user_skills"])
    @pytest.mark.asyncio
    async def test_empty_user_skills(
            self,
            oleg_id: uuid.UUID,
            oleg_users_rest_client: UsersRestClient,
    ):
        user_skills = set()

        skills = await oleg_users_rest_client.update_user_skills(
            user_id=oleg_id,
            skills=user_skills,
        )

        self.CONTEXT["skills"] = user_skills

        assert skills == user_skills

    @pytest.mark.dependency(depends=["TestUserSkillsFlow::test_empty_user_skills"])
    @pytest.mark.asyncio
    async def test_get_empty_user_skills(
            self,
            oleg_id: uuid.UUID,
            users_rest_client: UsersRestClient,
    ):
        user_skills: set[uuid.UUID] = self.CONTEXT["skills"]

        skills = await users_rest_client.get_user_skills(user_id=oleg_id)

        assert skills == user_skills
