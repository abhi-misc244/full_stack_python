import reflex as rx
from ..models import LoadModel, ProjectModel
from .state import LoadTableState


def load_input_page() -> rx.Component:
    return(
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
                            rx.table.column_header_cell("Equipment ID"),
                            rx.table.column_header_cell("Description"),
                            rx.table.column_header_cell("Voltage"),
                            rx.table.column_header_cell("Upstream Equipment ID"),
                            rx.table.column_header_cell("Power (kW)"),
                            rx.table.column_header_cell("Power Factor (Lag)"),
                            rx.table.column_header_cell("Efficiency"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(LoadTableState.loads,lambda load: rx.table.row
                            (                        
                                rx.table.row_header_cell(load.equip_id),
                                rx.table.cell(load.desc),
                                rx.table.cell(load.voltage),
                                rx.table.cell(load.u_equip_id),
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
        ),
    )

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

