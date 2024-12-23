import reflex as rx 

from ..ui.base import base_page

from . import state
from .notfound import project_not_found

from ..calculation.page import calculation_section

def project_detail_page() -> rx.Component:
    can_edit = True
    edit_link = rx.link("Edit", href=f"{state.ProjectState.project_edit_url}")
    edit_link_el = rx.cond(
        can_edit,
        edit_link,
        rx.fragment("")
    )
    my_child = rx.cond(
        state.ProjectState.project, 
        rx.vstack(
            rx.hstack(
                rx.heading(state.ProjectState.project.title, size="9"),
                edit_link_el,
                align='end'
            ),
            rx.text(
                state.ProjectState.project.description,
                white_space='pre-wrap'
            ),
            calculation_section(),  # Add the calculation section here
            spacing="5",
            align="center",
            min_height="85vh"
        ), 
        project_not_found()
    )
    return base_page(my_child)












