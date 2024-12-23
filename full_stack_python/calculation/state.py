# calculation/state.py
import reflex as rx
import pandas as pd
import reflex_local_auth.auth_session
from ..models import LoadModel, ProjectModel, UserInfo
from ..auth.state import SessionState
from sqlmodel import select
from ..project.state import ProjectState
from typing import Optional, List
from sqlalchemy import or_, cast, String

# Define the state class for loading the load entries
class LoadTableState(ProjectState):
    loads: List[LoadModel] = []
    #load: Optional['LoadModel'] = None

    search_value =""

    def load_loads(self, *args, **kwargs):
        print("Projects's user ID", self.project.userinfo_id)
        print("Projects's ID", self.project.id)
        print ("Users Userinfo ID", self.my_userinfo_id)
        lookups = (
            (LoadModel.project_id == self.proj_id) and
            (UserInfo.user_id == self.my_userinfo_id)
        )
        with rx.session() as session:
            result = session.exec(
                select(LoadModel).where(lookups)
            ).all()
            self.loads = result
            #print (result)
            



    def get_load_detail(self):
        if self.proj_id is None:
            self.load = None
            return 
        lookups = (
            (LoadModel.project_id == self.proj_id)
        )
        with rx.session() as session:
            if self.proj_id == "":
                self.load = None
                return
            sql_statement = select(LoadModel).where(lookups)
            result = session.exec(sql_statement).one_or_none()
            self.load = result            
            #print(result)
            return self.load
    
    @rx.event
    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries()
        #print (self.search_value)


    @rx.event
    def load_entries(self) -> list[LoadModel]:
        # Start with your base query including the initial filters
        with rx.session() as session:
            lookups = (
                (LoadModel.project_id == self.proj_id) and
                (UserInfo.user_id == self.my_userinfo_id)
            )
            query = select(LoadModel).where(lookups)

            # Add search filters if search value exists
            if self.search_value != "":
                search_value = (
                    f"%{self.search_value.lower()}%"
                )
                query = query.where(
                    or_(
                        cast(LoadModel.equip_id, String).ilike(search_value),
                        LoadModel.desc.ilike(search_value),
                        cast(LoadModel.power_kW, String).ilike(search_value),
                        cast(LoadModel.pf, String).ilike(search_value),
                        cast(LoadModel.eff, String).ilike(search_value),
                    )
                )
            self.loads = session.exec(query).all()
    

