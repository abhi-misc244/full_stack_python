import reflex as rx 
import reflex_local_auth
from ..ui.base import base_page


from . import forms

from .state import ProjectEditFormState
from .notfound import project_not_found

@reflex_local_auth.require_login
def project_edit_page() -> rx.Component:
    my_form = forms.project_edit_form()
    project = ProjectEditFormState.project
    my_child = rx.cond(project, 
            rx.vstack(
                rx.heading("Editing ", project.title, size="9"),
                rx.desktop_only(
                    rx.box(
                        my_form,
                        width='50vw'
                    )
                ),
                rx.tablet_only(
                    rx.box(
                        my_form,
                        width='75vw'
                    )
                ),
                rx.mobile_only(
                    rx.box(
                        my_form,
                        width='95vw'
                    )
                ),
                spacing="5",
                align="center",
                min_height="95vh",
            ), 
            project_not_found()
        )
    return base_page(my_child)