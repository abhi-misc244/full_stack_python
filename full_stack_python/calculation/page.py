# detail_page.py
import reflex as rx
from .. import navigation
from ..models import ProjectModel
from ..project.state import ProjectState
import reflex_local_auth

@reflex_local_auth.require_login
def calculation_section() -> rx.Component:
    current_project  = ProjectState.project
    return rx.vstack(
        rx.vstack(
            rx.text("Maximum Demand", weight="bold", size="6"),
            rx.text(
                "This will Calculate Maximum Demand of a site.",
                size="4",
                opacity=0.8,
                align="center",
            ),

        ),
        features(),
        maxdemand_name_return(current_project),
        spacing="6",
        border=f"1.5px solid {rx.color('gray', 5)}",
        background=rx.color("gray", 1),
        padding="28px",
        width="100%",
        max_width="400px",
        justify="center",
        border_radius="0.5rem",
    )


def maxdemand_name_return(current_project: ProjectModel):
    root_path = navigation.routes.PROJECTS_ROUTE
    project_id = current_project.id
    maxdemand_detail_url = f"{root_path}/{project_id}/calculation/maxdemand"

    return rx.link(
        rx.button("Get started",
                    
            size="3",
            variant="solid",
            width="100%",
            color_scheme="blue",
        ),
        href=maxdemand_detail_url,
    )
    






def feature_item(text: str) -> rx.Component:
    return rx.hstack(
        rx.icon("check", color=rx.color("accent", 9)),
        rx.text(text, size="4"),
    )


def features() -> rx.Component:
    return rx.vstack(
        feature_item("Power Factor Consumption at Each Bus."),
        feature_item("Load demand for different Scenarios."),
        feature_item("Dashboad Controls for selecting different buses."),
        feature_item("Common Data entry for Load flow and Short Circuit Analysis."),
        width="100%",
        align_items="start",
    )

