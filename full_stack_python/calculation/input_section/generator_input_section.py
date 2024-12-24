import reflex as rx
from ...models import GeneratorModel, ProjectModel
from ..states.GeneratorState import GeneratorTableState


def generator_input_page() -> rx.Component:
    return(
        rx.box(
            rx.vstack(
                rx.heading("Generator Inputs", size="4"),
                rx.input(
                    placeholder="Search here...",
                    on_change=lambda value: GeneratorTableState.filter_values(value),
                    width="25%",    
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Equipment ID"),
                            rx.table.column_header_cell("Description"),
                            rx.table.column_header_cell("Voltage"),
                            rx.table.column_header_cell("Phase"),
                            rx.table.column_header_cell("Power (kVA)"),
                            rx.table.column_header_cell("Power Factor (Lead)"),
                            rx.table.column_header_cell("Losses"),
                            rx.table.column_header_cell("Upstream Equipment ID"),
                            rx.table.column_header_cell("Operating Scenario"),
                            rx.table.column_header_cell("Swing Genrator"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(GeneratorTableState.generators,lambda generator: rx.table.row
                            (                        
                                rx.table.row_header_cell(generator.equip_id),
                                rx.table.cell(generator.desc),
                                rx.table.cell(generator.voltage),
                                rx.table.cell(generator.phase),
                                rx.table.cell(f"{(generator.power_kVA):.2f}"),
                                rx.table.cell(f"{(generator.pf):.2f}"),
                                rx.table.cell(f"{(generator.losses_per * 100):.2f}%"), # Shows 2 decimal places# Shows 2 decimal places
                                rx.table.cell(generator.u_equip_id),
                                rx.table.cell(generator.scenario),
                                rx.table.cell(generator.swing_gen),
                            ),
                        ),
                    ),
                    on_mount=GeneratorTableState.generator_entries,
                    width="100%",
                    spacing="7",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text("Select 'Swing Bus' Generator"),
                        rx.select(
                            GeneratorTableState.select_generator,
                            placeholder="Select Swing Generator",
                            on_change= GeneratorTableState.update_gen_values,
                        ),
                    ),
                    rx.hstack(
                        rx.button(
                            "Download as CSV",
                            on_click=GeneratorTableState.download_csv_data,
                        ),
                        rx.upload.root(
                            rx.button("Upload as CSV",),
                            on_drop=GeneratorTableState.upload_csv(rx.upload_files(upload_id="csv_upload")),
                            id="csv_upload"
                        ),
                        spacing="5",
                    ),
                    spacing="9",
                ),
                rx.vstack(
                    rx.text("Ensure all data is included in the CSV File when uploading. If data is not included, it will be removed.", font_size="0.75em"),
                    rx.text("Ony One generator can ge set as Swing Bus. When Swing Bus is changed, power factor will be defaulted to 0.9.", font_size="0.75em"),
                    spacing="2",  # Reduced spacing between text elements
                ),
                width='50vw',
                spacing="7",
            ),
            box_shadow="0px 10px 20px 0px rgba(0, 0, 0, 0.45)", 
            padding="2vw",
        ),
    )


