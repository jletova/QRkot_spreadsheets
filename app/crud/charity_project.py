from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            room_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_room_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == room_name
            )
        )
        return db_room_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> Optional[list]:
        projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    CharityProject.close_date,
                    CharityProject.create_date,
                    CharityProject.description
                ]
            ).where(
                CharityProject.fully_invested
            ).order_by(
                extract('year', self.model.close_date) - extract('year', self.model.create_date),
                extract('month', self.model.close_date) - extract('month', self.model.create_date),
                extract('day', self.model.close_date) - extract('day', self.model.create_date),
            )
        )
        return projects.all()


projects_crud = CRUDCharityProject(CharityProject)
