"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import reflex_local_auth

from rxconfig import config
from .ui.base import base_page

from .auth.state import SessionState
from . import contact, navigation, pages, project, calculation


from .auth.pages import (
    my_login_page,
    my_register_page,
    my_logout_page
)


def index() -> rx.Component:
    return base_page(
        rx.cond(SessionState.is_authenticated,
            pages.dashboard_component(),
            pages.landing_component(),
        )
    )



app = rx.App(
    theme=rx.theme(
        appearance="dark", 
        has_background=True, 
        panel_background="solid",
        scaling="90%",
        radius="medium", 
        accent_color="red"
    )

)

app.add_page(index,        
    )



# reflex_local_auth pages
app.add_page(my_login_page,
    route=reflex_local_auth.routes.LOGIN_ROUTE,
    title="Login",
)
app.add_page(my_register_page,
    route=reflex_local_auth.routes.REGISTER_ROUTE,
    title="Register",
)

app.add_page(my_logout_page,
    route=navigation.routes.LOGOUT_ROUTE,
    title="Logout",
)

# my pages
app.add_page(pages.about_page, 
             route=navigation.routes.ABOUT_US_ROUTE)

app.add_page(contact.contact_page, 
             route=navigation.routes.CONTACT_US_ROUTE)
app.add_page(
    contact.contact_entries_list_page, 
    route=navigation.routes.CONTACT_ENTRIES_ROUTE,
    on_load=contact.ContactState.list_entries
)

app.add_page(
    project.project_list_page, 
    route=navigation.routes.PROJECTS_ROUTE,
    on_load=project.ProjectState.load_projects
    
)

app.add_page(
    project.project_add_page, 
    route=navigation.routes.PROJECT_ADD_ROUTE
)

app.add_page(
    project.project_detail_page, 
    route="/project/[project_id]",
    on_load=project.ProjectState.get_project_detail
)

app.add_page(
    project.project_edit_page, 
    route="/project/[project_id]/edit",
    on_load=project.ProjectState.get_project_detail
)

app.add_page(
    calculation.maxdemand_page, 
    route="/project/[project_id]/calculation/maxdemand",
    on_load=calculation.LoadTableState.load_loads,
)
