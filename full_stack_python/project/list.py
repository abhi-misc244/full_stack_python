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


def project_name_return(project: ProjectModel):
    root_path = navigation.routes.PROJECTS_ROUTE
    project_id = project.id
    project_detail_url = f"{root_path}/{project_id}"
    return rx.link(
        rx.text(project.title),
        href=project_detail_url
    )


def project_auth_return(project: ProjectModel):
    return rx.text(project.userinfo.email)

def project_desc_return(project: ProjectModel):
    return rx.text(project.description)

def project_date_created_return(project: ProjectModel):
    return rx.text(project.created_at)



# def foreach_callback(text):
#     return rx.box(rx.text(text))

@reflex_local_auth.require_login
def project_list_page() ->rx.Component:
    # Define columns for the data table 
    return base_page(
        rx.vstack(
            rx.heading("Project List",  size="5"),
            rx.link(
                rx.button("New Project"),
                href=navigation.routes.PROJECT_ADD_ROUTE
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Project name"),
                        rx.table.column_header_cell("Author Email"),
                        rx.table.column_header_cell("Project Description"),
                        rx.table.column_header_cell("Date Created"),
                    ),
                ),
                rx.table.body(
                    rx.table.row(
                        rx.table.row_header_cell(rx.foreach(state.ProjectState.projects, project_name_return)),
                        rx.table.cell(rx.foreach(state.ProjectState.projects, project_auth_return)),
                        rx.table.cell(rx.foreach(state.ProjectState.projects, project_desc_return)),
                        rx.table.cell(rx.foreach(state.ProjectState.projects, project_date_created_return)),
                    ),
                ),
            ),
            spacing="5",
            align="center",
            min_height="85vh",
        ),
    ) 

'''# rx.foreach(["abc", "abc", "cde"], foreach_callback),
rx.foreach(state.ProjectState.projects, project_list_item),'''
