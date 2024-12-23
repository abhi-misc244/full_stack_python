import reflex as rx 
import reflex_local_auth
from ..ui.base import base_page
from ..project.state import ProjectState
#from .state import LoadTableState
import pandas as pd
from ..models import LoadModel, ProjectModel
from ..project.notfound import project_not_found
from .load_input_section import load_input_page

@reflex_local_auth.require_login
def maxdemand_page() -> rx.Component:
    page_title = "Maximum Demand for " + ProjectState.project.title
    #load_table = LoadTableState.loading_load_data_table
    #print("Checking this ",LoadTableState.loads)
    my_child = rx.cond(
        ProjectState.project,
        rx.vstack(
            rx.heading(page_title, size="6"),
            load_input_page(),

            spacing="9",
            align="center",
            min_height="85vh"
        ),
        project_not_found()
    )
    return base_page(my_child)


'''def load_equipID_return(load: LoadModel):
    return rx.text(load.equip_id)

def load_desc_return(load: LoadModel):
    return rx.text(load.desc)

def load_powerKW_return(load: LoadModel):
    return rx.text(load.power_kW)

def load_pf_return(load: LoadModel):
    return rx.text(load.pf)

def load_eff_return(load: LoadModel):
    return rx.text(load.eff)'''


'''
            rx.box(
                rx.vstack(
                    rx.heading("Load Inputs", size="4"),
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
                        spacing="7",
                    ),
                    rx.hstack(
                        rx.button(
                            "Download as CSV",
                            on_click=LoadTableState.download_csv_data,
                        ),
                        rx.upload.root(
                            rx.button("Upload as CSV",),
                            on_drop=LoadTableState.upload_csv(rx.upload_files(upload_id="csv_upload")),
                            id="csv_upload"
                        ),
                        spacing="5",
                    ),
                    rx.text("Ensure all data is included in the CSV File when uploading. If data is not included, it will be removed."),
                    width='50vw',
                    spacing="7",
                ),
                box_shadow="0px 10px 20px 0px rgba(0, 0, 0, 0.45)", 
                padding="2vw",
            ),'''



