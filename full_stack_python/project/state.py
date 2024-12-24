from datetime import datetime
from typing import Optional, List
import reflex as rx 

import sqlalchemy
from sqlmodel import select

from .. import navigation
from ..auth.state import SessionState
from ..models import ProjectModel, UserInfo, LoadModel, BusModel, GeneratorModel, PowerNetworkModel

PROJECTS_ROUTE = navigation.routes.PROJECTS_ROUTE
if PROJECTS_ROUTE.endswith("/"):
    PROJECTS_ROUTE = PROJECTS_ROUTE[:-1]

class ProjectState(SessionState):
    projects: List['ProjectModel'] = []
    project: Optional['ProjectModel'] = None
    project_description: str = ""
    project_publish_active: bool = False

    @rx.var
    def proj_id(self):
        return self.router.page.params.get("project_id", "")

    '''@rx.var
    def project_url(self):
        if not self.project:
            return f"{PROJECTS_ROUTE}"
        return f"{PROJECTS_ROUTE}/{self.project.id}"'''
    
    @rx.var
    def project_url(self):
        if not self.project:
            return f"{PROJECTS_ROUTE}"
        with rx.session() as session:
            # Refresh the project instance within session scope
            project = session.merge(self.project)
            session.refresh(project)
            if project is None:
                return f"{PROJECTS_ROUTE}"
            return f"{PROJECTS_ROUTE}/{project.id}"

    '''@rx.var
    def project_edit_url(self):
        if not self.project:
            return f"{PROJECTS_ROUTE}"
        return f"{PROJECTS_ROUTE}/{self.project.id}/edit"'''
    
    @rx.var
    def project_edit_url(self):
        if not self.project:
            return f"{PROJECTS_ROUTE}"
        with rx.session() as session:
            project = session.merge(self.project)
            session.refresh(project)
            if project is None:
                return f"{PROJECTS_ROUTE}"
            return f"{PROJECTS_ROUTE}/{project.id}/edit"
    



    def get_project_detail(self):
        if self.my_userinfo_id is None:
            self.project = None
            self.project_description = ""
            self.project_publish_active = False
            return 
        lookups = (
            (ProjectModel.userinfo_id == self.my_userinfo_id) &
            (ProjectModel.id == self.proj_id)
        )
        with rx.session() as session:
            if self.proj_id == "":
                self.project = None
                return
            sql_statement = select(ProjectModel).options(
                sqlalchemy.orm.joinedload(ProjectModel.userinfo).joinedload(UserInfo.user)
            ).where(lookups)
            result = session.exec(sql_statement).one_or_none()
            # if result.userinfo: # db lookup
            #     print('working')
            #     result.userinfo.user # db lookup
            self.project = result
            if result is None:
                self.project_description = ""
                return
            self.project_description = self.project.description
            self.project_publish_active = self.project.publish_active
        # return


    def load_projects(self, *args, **kwargs):
        # if published_only:
        #     lookup_args = ( 
        #         (ProjectModel.publish_active == True) &
        #         (ProjectModel.publish_date < datetime.now())
        #     )
        with rx.session() as session:
            result = session.exec(
                select(ProjectModel).options(
                    sqlalchemy.orm.joinedload(ProjectModel.userinfo)
                ).where(ProjectModel.userinfo_id == self.my_userinfo_id)
            ).all()
            self.projects = result
        # return

    def add_project(self, form_data:dict):
        with rx.session() as session:
            project = ProjectModel(**form_data)
            # print("adding", project)
            session.add(project)
            session.commit()
            session.refresh(project) # project.id

            # Add three sample loads 
            sample_loads = [
                LoadModel(equip_id='1', desc="Sample Load 1", power_kW=10.0, pf=0.9, eff=0.85, voltage=415, phase =3, duty=0.8, scenario='A', u_equip_id='SB001', project_id=project.id), 
                LoadModel(equip_id='2', desc="Sample Load 2", power_kW=20.0, pf=0.95, eff=0.90, voltage=415, phase =3, duty=0.8, scenario='A', u_equip_id='SB002', project_id=project.id), 
                LoadModel(equip_id='3', desc="Sample Load 3", power_kW=30.0, pf=0.85, eff=0.80, voltage=415, phase =3, duty=0.8, scenario='A', u_equip_id='SB002', project_id=project.id), 
                ] 
            session.add_all(sample_loads) 

            # Add two sample Buses
            sample_buses = [
                BusModel(equip_id='SB001', desc="Sample Switchboard No 1", losses_per=.01, voltage=415, phase =3, scenario='A', u_equip_id='GRID01', project_id=project.id), 
                BusModel(equip_id='SB002', desc="Sample Switchboard No 2", losses_per=.01, voltage=415, phase =3, scenario='A', u_equip_id='SB001', project_id=project.id), 
                ] 
            session.add_all(sample_buses)

            # Add two sample Generators
            sample_generators = [
                GeneratorModel(equip_id='GRID01', desc="Grid Connection No. 1", power_kVA=10.0, pf=0.9, eff=0.85, losses_per=.01, voltage=415, phase =3, scenario='A', u_equip_id='N/A', project_id=project.id, swing_gen=True), 
                GeneratorModel(equip_id='CAP01', desc="Sample Capacitor Bank", power_kVA=10.0, pf=1, eff=0.85, losses_per=.01, voltage=415, phase =3, scenario='A', u_equip_id='SB002', project_id=project.id, swing_gen=False), 
                ] 
            session.add_all(sample_generators)

            # Create network connections for each load
            network_connections = []
            for load in sample_loads:
                network_connections.append(
                    PowerNetworkModel(
                        load_eq_id=load.equip_id,
                        bus_eq_id=None,  
                        project_id=project.id
                    )
                )
            for generator in sample_generators:
                network_connections.append(
                    PowerNetworkModel(
                        load_eq_id=None,
                        gen_eq_id=generator.equip_id,  
                        bus_eq_id=None,
                        project_id=project.id
                    )
                )
            for bus in sample_buses:
                network_connections.append(
                    PowerNetworkModel(
                        load_eq_id=None,
                        gen_eq_id=None,
                        bus_eq_id=bus.equip_id,  
                        project_id=project.id
                    )
                )
            session.add_all(network_connections)



            session.commit()
            # Refresh project one final time after all operations
            session.refresh(project)
            # Assign to state within session
            self.project = project


    def save_project_edits(self, project_id:int, updated_data:dict):
        with rx.session() as session:
            project = session.exec(
                select(ProjectModel).where(
                    ProjectModel.id == project_id
                )
            ).one_or_none()
            if project is None:
                return
            for key, value in updated_data.items():
                setattr(project, key, value)
            session.add(project)
            session.commit()
            session.refresh(project)
            self.project = project
    
    def to_project(self, edit_page=False):
        if not self.project:
            return rx.redirect(PROJECTS_ROUTE)
        if edit_page:
             return rx.redirect(f"{self.project_edit_url}")
        return rx.redirect(f"{self.project_url}")


class ProjectAddFormState(ProjectState):
    form_data: dict = {}

    def handle_submit(self, form_data):
        data = form_data.copy()
        if self.my_userinfo_id is not None:
            data['userinfo_id'] = self.my_userinfo_id
        self.form_data = data
        self.add_project(data)
        return self.to_project(edit_page=True)


class ProjectEditFormState(ProjectState):
    form_data: dict = {}
    # project_description: str = ""

    @rx.var
    def publish_display_date(self) -> str:
        # return "2023-12-01" # YYYY-MM-DD
        if not self.project:
            return datetime.now().strftime("%Y-%m-%d")
        if not self.project.publish_date:
            return datetime.now().strftime("%Y-%m-%d")
        return self.project.publish_date.strftime("%Y-%m-%d")
    
    @rx.var
    def publish_display_time(self) -> str:
        if not self.project:
            return datetime.now().strftime("%H:%M:%S")
        if not self.project.publish_date:
            return datetime.now().strftime("%H:%M:%S")
        return self.project.publish_date.strftime("%H:%M:%S")

    def handle_submit(self, form_data):
        self.form_data = form_data
        project_id = form_data.pop('project_id')
        publish_date = None
        if 'publish_date' in form_data:
            publish_date = form_data.pop('publish_date')
        publish_time = None
        if 'publish_time' in form_data:
            publish_time = form_data.pop('publish_time')
        publish_input_string = f"{publish_date} {publish_time}"
        try:
            final_publish_date = datetime.strptime(publish_input_string, '%Y-%m-%d %H:%M:%S')
        except:
            final_publish_date = None
        publish_active = False
        if 'publish_active' in form_data:
            publish_active = form_data.pop('publish_active') == "on"
        updated_data = {**form_data}
        updated_data['publish_active'] = publish_active
        updated_data['publish_date'] = final_publish_date
        self.save_project_edits(project_id, updated_data)
        return self.to_project()

