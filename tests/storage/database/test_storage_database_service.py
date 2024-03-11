from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import desc, or_, select

from sapphire.database.models import SpecializationGroup
from sapphire.storage.database import Service


@pytest.mark.asyncio
async def test_get_specialization_groups_without_filters(service: Service):
    session = MagicMock()
    name = "Developer"
    page = 1
    per_page = 10
    offset = (page - 1) * per_page

    expected_specialization_groups = [SpecializationGroup(name=name)]
    mock_specialization_group = MagicMock()
    mock_specialization_group.unique().scalars.return_value.all.return_value = (
        expected_specialization_groups
    )

    session.execute = AsyncMock(return_value=mock_specialization_group)

    expected_query = (
        select(SpecializationGroup)
        .order_by(desc(SpecializationGroup.created_at))
        .limit(per_page)
        .offset(offset)
    )

    specialization_groups = await service.get_specialization_groups(session=session)

    assert specialization_groups == expected_specialization_groups
    
    query = session.execute.call_args_list[0].args[0]
    assert expected_query.compare(query)


@pytest.mark.asyncio
async def test_get_specialization_groups_with_all_filters(service: Service):
    session = MagicMock()
    name = "Developer"
    page = 1
    per_page = 10
    offset = (page - 1) * per_page

    expected_specialization_groups = [SpecializationGroup(name=name)]
    mock_specialization_group = MagicMock()
    mock_specialization_group.unique().scalars.return_value.all.return_value = (
        expected_specialization_groups
    )

    session.execute = AsyncMock(return_value=mock_specialization_group)

    expected_query = (
        select(SpecializationGroup)
        .order_by(desc(SpecializationGroup.created_at))
        .where(or_(
            SpecializationGroup.name.icontains(name),
            SpecializationGroup.name_en.icontains(name),
        ))
        .limit(per_page)
        .offset(offset)
    )

    specialization_groups = await service.get_specialization_groups(
        session=session,
        query_text=name,
        page=page,
        per_page=per_page,
    )

    assert specialization_groups == expected_specialization_groups
    
    query = session.execute.call_args_list[0].args[0]
    assert expected_query.compare(query)
