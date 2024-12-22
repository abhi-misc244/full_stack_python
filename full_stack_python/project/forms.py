import reflex as rx 


from .state import (
    ProjectAddFormState,
    ProjectEditFormState
)


def project_add_form() -> rx.Component:
    return rx.form(
            rx.vstack(
                rx.hstack(
                    rx.input(
                        name="title",
                        placeholder="Title",
                        required=True,
                        type='text',
                        width='100%',
                    ),
                    width='100%'
                ),
                rx.text_area(
                    name='description',
                    placeholder="Your message",
                    required=True,
                    height='50vh',
                    width='100%',
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=ProjectAddFormState.handle_submit,
            reset_on_submit=True,
    )




def project_edit_form() -> rx.Component:
    project = ProjectEditFormState.project
    title = project.title
    publish_active = project.publish_active
    project_description = ProjectEditFormState.project_description
    return rx.form(
            rx.box(
                rx.input(
                    type='hidden',
                    name='project_id',
                    value=project.id
                ),
                display='none'
            ), 
            rx.vstack(
                rx.hstack(
                    rx.input(
                        default_value=title,
                        name="title",
                        placeholder="Project Title",
                        required=True,
                        type='text',
                        width='100%',
                    ),
                    width='100%'
                ),
                rx.text_area(
                    value = project_description,
                    on_change = ProjectEditFormState.set_project_description,
                    name='description',
                    placeholder="Project Description",
                    required=True,
                    height='20vh',
                    width='100%',
                ),
                rx.flex(
                    rx.switch(
                        default_checked=ProjectEditFormState.project_publish_active,
                        on_change=ProjectEditFormState.set_project_publish_active,
                        name='project_active',          
                    ),
                    rx.text("Project Active"),
                    spacing="2",
                ),
                rx.cond(
                    ProjectEditFormState.project_publish_active,
                    rx.box(
                        rx.hstack(
                            rx.input(
                                default_value=ProjectEditFormState.publish_display_date,
                                type='date',
                                name='publish_date',
                                width='100%'
                            ),
                            rx.input(
                                default_value=ProjectEditFormState.publish_display_time,
                                type='time',
                                 name='publish_time',
                                width='100%'
                            ),
                        width='100%'
                        ),
                        width='100%'
                    )
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=ProjectEditFormState.handle_submit,
    )


