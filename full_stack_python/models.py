from typing import Optional, List
from datetime import datetime
import reflex as rx
from reflex_local_auth.user import LocalUser

import sqlalchemy
from sqlmodel import Field, Relationship

from . import utils

class UserInfo(rx.Model, table=True):
    email: str
    user_id: int = Field(foreign_key='localuser.id')
    user: LocalUser | None = Relationship() # LocalUser instance
    projects: List['ProjectModel'] = Relationship(
        back_populates='userinfo'
    )
    
    contact_entries: List['ContactEntryModel'] = Relationship(
        back_populates='userinfo'
    )

    '''project_entries: List['ProjectEntryModel'] = Relationship(
        back_populates='userinfo'
    )'''
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': sqlalchemy.func.now(),
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )


class ContactEntryModel(rx.Model, table=True):
    user_id: int | None = None
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    userinfo: Optional['UserInfo'] = Relationship(back_populates="contact_entries")
    first_name: str
    last_name: str | None = None
    email: str | None = None # = Field(nullable=True)
    message: str
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )



class ProjectModel(rx.Model, table=True):
    # user
    # id: int -> primary key
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    userinfo: Optional['UserInfo'] = Relationship(back_populates="projects")
    title: str
    description: str
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': sqlalchemy.func.now(),
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )
    publish_active: bool = False
    publish_date: datetime = Field(
        default=None,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={},
        nullable=True
    )
    # Add the back_populates relationship in the ProjectModel
    loads: list['LoadModel'] = Relationship(back_populates="project")


class LoadModel(rx.Model, table=True):
    equip_id: str
    desc: Optional[str] = None  # Make it nullable
    power_kW: Optional[float] = None  # Make it nullable
    pf: Optional[float] = None  # Make it nullable
    eff: Optional[float] = None  # Make it nullable
    voltage: Optional[float] = None  # Make it nullable
    u_equip_id: str

    project_id: int = Field(default=None, foreign_key="projectmodel.id")
    project: Optional['ProjectModel'] = Relationship(back_populates="loads")

