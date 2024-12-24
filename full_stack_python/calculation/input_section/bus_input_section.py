import reflex as rx
from ...models import BusModel, ProjectModel
from ..states.BusState import BusTableState


def bus_input_page() -> rx.Component:
    return(
        rx.box(
            rx.vstack(
                rx.heading("Bus Inputs", size="4"),
                rx.input(
                placeholder="Search here...",
                on_change=lambda value: BusTableState.filter_values(value),
                width="25%",    
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Equipment ID"),
                            rx.table.column_header_cell("Description"),
                            rx.table.column_header_cell("Voltage"),
                            rx.table.column_header_cell("Phase"),
                            rx.table.column_header_cell("Losses"),
                            rx.table.column_header_cell("Upstream Equipment ID"),
                            rx.table.column_header_cell("Operating Scenario"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(BusTableState.buses,lambda bus: rx.table.row
                            (                        
                                rx.table.row_header_cell(bus.equip_id),
                                rx.table.cell(bus.desc),
                                rx.table.cell(bus.voltage),
                                rx.table.cell(bus.phase),
                                rx.table.cell(f"{(bus.losses_per * 100):.2f}%"), # Shows 2 decimal places# Shows 2 decimal places
                                rx.table.cell(bus.u_equip_id),
                                rx.table.cell(bus.scenario),
                            ),
                        ),
                    ),
                    on_mount=BusTableState.bus_entries,
                    width="100%",
                    spacing="7",
                ),
                rx.hstack(
                    rx.button(
                        "Download as CSV",
                        on_click=BusTableState.download_csv_data,
                    ),
                    rx.upload.root(
                        rx.button("Upload as CSV",),
                        on_drop=BusTableState.upload_csv(rx.upload_files(upload_id="csv_upload")),
                        id="csv_upload"
                    ),
                    spacing="5",
                ),
                rx.text("Ensure all data is included in the CSV File when uploading. If data is not included, it will be removed.", font_size="0.75em"),
                width='50vw',
                spacing="7",
            ),
            box_shadow="0px 10px 20px 0px rgba(0, 0, 0, 0.45)", 
            padding="2vw",
        ),
    )


