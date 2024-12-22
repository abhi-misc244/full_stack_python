# calculation/state.py
import reflex as rx
import pandas as pd
from ..models import LoadModel
from sqlmodel import select
from ..project.state import ProjectState
from typing import Optional, List

# Define the state class for loading the load entries
class LoadTableState(ProjectState):
    loads: List[LoadModel] = []
    #load: Optional['LoadModel'] = None

    def load_loads(self, *args, **kwargs):
        with rx.session() as session:
            result = session.exec(
                select(LoadModel).where(LoadModel.project_id == self.proj_id)
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


    '''@rx.var
    def load_entries(self) -> list[LoadModel]:
        """Get all loads for a specific project from the database."""
        with rx.session() as session:
            results = session.exec(
                select(LoadModel).where(LoadModel.project_id == ProjectState.proj_id)
                ).all()
            
            self.loads = [
                results.dict() for result in results]'''
    
    '''def show_load(load: list):
        """Show a perloadson in a table row."""
        return rx.table.row(
            rx.table.cell(load[0]),
            
        )


    def loading_load_data_table():
            return rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Equip ID"),
                        rx.table.column_header_cell("Description"),
                        rx.table.column_header_cell("Power (kW)"),
                        rx.table.column_header_cell("Power Factor"),
                        rx.table.column_header_cell("Efficiency"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        LoadTableState.loads, "Testing"
                    )
                ),
                #on_mount=LoadTableState.load_entries(ProjectState.project.id),
                width="100%",
            )


    
    def load_entries(self) -> list[LoadModel]:
        """Get all loads for a specific project from the database."""
        with rx.session() as session:            
            query = select(LoadModel)            
            query = query.where(LoadModel.project_id == 4)
            return session.exec(query).all()'''



    

