import reflex as rx 
import reflex_local_auth
from .. import navigation
from ..ui.base import base_page
from ..models import ProjectModel
from . import state

def project_detail_link(child: rx.Component, project: ProjectModel):
    if project is None:
        return rx.fragment(child)
    project_id = project.id
    if project_id is None:
        return rx.fragment(child)
    root_path = navigation.routes.PROJECTS_ROUTE
    project_detail_url = f"{root_path}/{project_id}"
    return rx.link(
        child,
        rx.heading("by ", project.userinfo.email),
        href=project_detail_url
    )

def project_list_item(project: ProjectModel):
    return rx.box(
        project_detail_link(
            rx.heading(project.title),
            
            project
        ),
        padding='1em'
    )

# def foreach_callback(text):
#     return rx.box(rx.text(text))

@reflex_local_auth.require_login
def project_list_page() ->rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Project List",  size="5"),
            rx.link(
                rx.button("New Project"),
                href=navigation.routes.PROJECT_ADD_ROUTE
            ),
            # rx.foreach(["abc", "abc", "cde"], foreach_callback),
            rx.foreach(state.ProjectState.projects, project_list_item),
            spacing="5",
            align="center",
            min_height="85vh",
        )
    ) 