import reflex as rx 
import reflex_local_auth
from ..ui.base import base_page
from ..project.state import ProjectState
from .state import LoadTableState
import pandas as pd
from ..models import LoadModel, ProjectModel
from ..project.notfound import project_not_found

@reflex_local_auth.require_login
def maxdemand_page() -> rx.Component:
    page_title = "Calculate Maximum Demand of " + ProjectState.project.title
    #load_table = LoadTableState.loading_load_data_table
    #print("Checking this ",LoadTableState.loads)
    my_child = rx.cond(
        ProjectState.project,
        rx.vstack(
            rx.heading(page_title, size="9"),
            rx.box(
                rx.input(
                    placeholder="Search here...",
                    on_change=lambda value: LoadTableState.filter_values(value),
                width="25%",    
                ),
                rx.table.root(
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
                        rx.foreach(LoadTableState.loads,lambda load: rx.table.row
                            (                        
                                rx.table.row_header_cell(load.equip_id),
                                rx.table.cell(load.desc),
                                rx.table.cell(load.power_kW),
                                rx.table.cell(load.pf),
                                rx.table.cell(load.eff),
                            ),
                        ),
                    ),
                    on_mount=LoadTableState.load_entries,
                    width="100%",
                ),
                width='50vw',
            ),
            spacing="5",
            align="center",
            min_height="85vh"
        ),
        project_not_found()
    )
    return base_page(my_child)

'''        rx.vstack(
        rx.heading(page_title, size="9"),
        rx.desktop_only(            
            rx.box(
                #rx.text(ProjectState.project.id),
                #rx.text(ProjectState.project.title),
                #rx.text(LoadTableState.loads),
                #load_table,

                rx.table.root(
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
                        rx.foreach(LoadTableState.loads,lambda load: rx.table.row
                            (                        
                                rx.table.row_header_cell(load.equip_id),
                                rx.table.cell(load.desc),
                                rx.table.cell(load.power_kW),
                                rx.table.cell(load.pf),
                                rx.table.cell(load.eff),
                            ),
                        ),
                    ),
                    #on_mount=LoadTableState.load_entries(ProjectState.project.id),
                    width="100%",
                ),
                width='50vw',
            ),
        ),
        rx.tablet_only(
            rx.box(
                #load_table,
                width='75vw',
            ),
        ),
        rx.mobile_only(
            rx.box(
                #load_table,
                width='95vw',
            ),
        ),
        spacing="5",
        align="center",
        min_height="95vh",
    )'''


def load_equipID_return(load: LoadModel):
    print("This is it", load)
    print("This is it", load.desc)
    #print (load.get_load_detail.equip_id)
    return rx.text(load.equip_id)

def load_desc_return(load: LoadModel):
    return rx.text(load.desc)

def load_powerKW_return(load: LoadModel):
    return rx.text(load.power_kW)

def load_pf_return(load: LoadModel):
    return rx.text(load.pf)

def load_eff_return(load: LoadModel):
    return rx.text(load.eff)



