import reflex as rx 
import reflex_local_auth
from ..ui.base import base_page
from ..project.state import ProjectState
import pandas as pd
from ..models import LoadModel, ProjectModel
from ..project.notfound import project_not_found
from .input_section import load_input_section, bus_input_section, generator_input_section


@reflex_local_auth.require_login
def maxdemand_page() -> rx.Component:
    page_title = "Maximum Demand for " + ProjectState.project.title
    my_child = rx.cond(
        ProjectState.project,
        rx.vstack(
            rx.heading(page_title, size="6"),
            generator_input_section.generator_input_page(),
            bus_input_section.bus_input_page(),
            load_input_section.load_input_page(),
            spacing="9",
            align="center",
            min_height="85vh"
        ),
        project_not_found()
    )
    return base_page(my_child)



