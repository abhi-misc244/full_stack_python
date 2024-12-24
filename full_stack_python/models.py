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

    # Add the back_populates relationship in the ProjectModel
    buses: list['BusModel'] = Relationship(back_populates="project")

    # Add the back_populates relationship in the ProjectModel
    generators: list['GeneratorModel'] = Relationship(back_populates="project")

    # Add the back_populates relationship in the ProjectModel
    powernetwork: list['PowerNetworkModel'] = Relationship(back_populates="project")

class LoadModel(rx.Model, table=True):
    equip_id: str
    desc: Optional[str] = None  # Make it nullable
    power_kW: Optional[float] = None  # Make it nullable
    pf: Optional[float] = None  # Make it nullable
    eff: Optional[float] = None  # Make it nullable
    voltage: Optional[float] = None  # Make it nullable
    phase: int = Field(default=3)
    u_equip_id: str
    duty: Optional[float] = None  # Make it nullable
    scenario: Optional[str] = None  # Make it nullable

    project_id: int = Field(default=None, foreign_key="projectmodel.id")
    project: Optional['ProjectModel'] = Relationship(back_populates="loads")

    # Add the back_populates relationship in the PowerNetworkModel
    powernetwork: Optional['PowerNetworkModel'] = Relationship(back_populates="load")


class BusModel(rx.Model, table=True):
    equip_id: str
    desc: Optional[str] = None  # Make it nullable
    losses_per: Optional[float] = None  # Make it nullable
    voltage: Optional[float] = None  # Make it nullable
    phase: int = Field(default=3)
    u_equip_id: str
    scenario: Optional[str] = None  # Make it nullable

    project_id: int = Field(default=None, foreign_key="projectmodel.id")
    project: Optional['ProjectModel'] = Relationship(back_populates="buses")

    # Add the back_populates relationship in the PowerNetworkModel
    powernetwork: Optional['PowerNetworkModel'] = Relationship(back_populates="bus") 



class GeneratorModel(rx.Model, table=True):
    equip_id: str
    desc: Optional[str] = None  # Make it nullable
    power_kVA: Optional[float] = None  # Make it nullable
    losses_per: Optional[float] = None  # Make it nullable
    pf: Optional[float] = None  # Make it nullable
    voltage: Optional[float] = None  # Make it nullable
    phase: int = Field(default=3)
    u_equip_id: str
    scenario: Optional[str] = None  # Make it nullable
    swing_gen: bool = Field(default=False)

    project_id: int = Field(default=None, foreign_key="projectmodel.id")
    project: Optional['ProjectModel'] = Relationship(back_populates="generators")

    # Add the back_populates relationship in the PowerNetworkModel
    powernetwork: Optional['PowerNetworkModel'] = Relationship(back_populates="generator") 


class PowerNetworkModel(rx.Model, table=True):
    
    gen_eq_id: str = Field(default=None, foreign_key="generatormodel.equip_id")
    load_eq_id: str = Field(default=None, foreign_key="loadmodel.equip_id")
    bus_eq_id: str = Field(default=None, foreign_key="busmodel.equip_id")
    project_id: int = Field(default=None, foreign_key="projectmodel.id")

    project: ProjectModel = Relationship(back_populates="powernetwork")
    load: LoadModel = Relationship(back_populates="powernetwork")
    generator: GeneratorModel = Relationship(back_populates="powernetwork")
    bus: BusModel = Relationship(back_populates="powernetwork")

    def __init__(self, **kwargs): 
        super().__init__(**kwargs) 
        self.trigger_properties()

    def trigger_properties(self):
        _ = self.voltage
        _ = self.equip_id 
        _ = self.flc

    @property
    def voltage(self) -> float:
        if self.generator and self.generator.voltage is not None:
            return self.generator.voltage
        elif self.load and self.load.voltage is not None:
            return self.load.voltage
        elif self.bus and self.bus.voltage is not None:
            return self.bus.voltage
        return None

    @property
    def equip_id(self) -> float:
        if self.generator and self.generator.equip_id is not None:
            return self.generator.equip_id
        elif self.load and self.load.equip_id is not None:
            return self.load.equip_id
        elif self.bus and self.bus.equip_id is not None:
            return self.bus.equip_id
        return None
    
    @property
    def flc(self) -> float:
        if self.generator and self.generator.equip_id is not None:
            return ((self.generator.power_kVA))/((self.generator.voltage)* (3)**.5)
        elif self.load and self.load.power_kW is not None:
            return ((self.load.power_kW)/self.load.pf)/((self.load.voltage)* (3)**.5)
        elif self.bus and self.bus.equip_id is not None:
            return 0
        return None

    






