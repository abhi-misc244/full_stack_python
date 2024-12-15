import reflex as rx 

from ..ui.base import base_page

from . import state
from .notfound import project_not_found
# @rx.page(route='/about')
def project_detail_page() -> rx.Component:
    can_edit = True
    edit_link = rx.link("Edit", href=f"{state.ProjectState.project_edit_url}")
    edit_link_el = rx.cond(
        can_edit,
        edit_link,
        rx.fragment("")
    )
    my_child = rx.cond(state.ProjectState.project, rx.vstack(
            rx.hstack(
                rx.heading(state.ProjectState.project.title, size="9"),
                edit_link_el,
                align='end'
            ),
            rx.text("User info id ", state.ProjectState.project.userinfo_id),
            rx.text("User info: ", state.ProjectState.project.userinfo.to_string()),
            rx.text("User: ", state.ProjectState.project.userinfo.user.to_string()),
            rx.text(state.ProjectState.project.publish_date),
            rx.text(
                state.ProjectState.project.description,
                white_space='pre-wrap'
            ),
            spacing="5",
            align="center",
            min_height="85vh"
        ), 
        project_not_found()
        )
    return base_page(my_child)