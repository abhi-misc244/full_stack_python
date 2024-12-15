'''import reflex as rx 
from ..ui.base import base_page
from ..models import ProjectEntryModel
from . import form, state

def project_entry_list_item(project: ProjectEntryModel):
    return rx.box(
        rx.heading(project.project_name),
        rx.text("Message:", project.project_description),
        rx.cond(project.user_id, 
                rx.text("User Id:", f"{project.user_id}",), 
                rx.fragment("")),
        padding='1em'
    )

# def foreach_callback(text):
#     return rx.box(rx.text(text))

def project_entries_list_page() ->rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Add New Project", size="5"),
            # rx.foreach(["abc", "abc", "cde"], foreach_callback),
            rx.foreach(state.ProjectState.entries, project_entry_list_item),
            spacing="5",
            align="center",
            min_height="85vh",
        )
    ) 

def project_page() -> rx.Component:
    
    my_child = rx.vstack(
            rx.heading("Your Projects", size="9"),
            rx.cond(state.ProjectState.did_submit, state.ProjectState.thank_you, ""),
            rx.desktop_only(
                rx.box(
                    form.project_form(),
                    width='50vw'
                )
            ),
            rx.tablet_only(
                rx.box(
                    form.project_form(),
                    width='75vw'
                )
            ),
            rx.mobile_only(
                rx.box(
                    form.project_form(),
                    width='95vw'
                )
            ),
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
            id='my-child'
        )
    return base_page(my_child)'''