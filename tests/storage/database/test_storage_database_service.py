from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import desc, or_, select

from sapphire.storage.database.models import SpecializationGroup
from sapphire.storage.database.service import StorageDatabaseService


@pytest.mark.asyncio
async def test_get_specialization_groups_without_filters(database_service: StorageDatabaseService):
    session = MagicMock()
    name = "Developer"

    expected_specialization_groups = [SpecializationGroup(name=name)]
    mock_specialization_group = MagicMock()
    mock_specialization_group.unique().scalars.return_value.all.return_value = (
        expected_specialization_groups
    )

    session.execute = AsyncMock(return_value=mock_specialization_group)

    expected_query = select(SpecializationGroup).order_by(desc(SpecializationGroup.created_at))

    specialization_groups = await database_service.get_specialization_groups(session=session)

    assert specialization_groups == expected_specialization_groups
    
    query = session.execute.call_args_list[0].args[0]
    assert expected_query.compare(query)


@pytest.mark.asyncio
async def test_get_specialization_groups_with_all_filters(
    database_service: StorageDatabaseService
):
    session = MagicMock()
    name = "Developer"
    cursor = datetime.now()
    per_page = 10

    expected_specialization_groups = [SpecializationGroup(name=name)]
    mock_specialization_group = MagicMock()
    mock_specialization_group.unique().scalars.return_value.all.return_value = (
        expected_specialization_groups
    )

    session.execute = AsyncMock(return_value=mock_specialization_group)

    expected_query = (
        select(SpecializationGroup)
        .order_by(desc(SpecializationGroup.created_at))
        .where(
            or_(
                SpecializationGroup.name.contains(name),
                SpecializationGroup.name_en.contains(name),
            ),
            SpecializationGroup.created_at < cursor,
        )
        .limit(per_page)
    )

    specialization_groups = await database_service.get_specialization_groups(
        session=session,
        query_text=name,
        cursor=cursor,
        per_page=per_page,
    )

    assert specialization_groups == expected_specialization_groups
    
    query = session.execute.call_args_list[0].args[0]
    assert expected_query.compare(query)
