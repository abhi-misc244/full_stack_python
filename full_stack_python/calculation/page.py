# detail_page.py
import reflex as rx
from .state import CalculationState

def calculation_section() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.text("Calculation No. 1", weight="bold", size="6"),
            rx.text(
                "This will Calculate xxxx",
                size="4",
                opacity=0.8,
                align="center",
            ),

        ),
        features(),
        rx.button(
            "Get started",
            size="3",
            variant="solid",
            width="100%",
            color_scheme="blue",
        ),
        spacing="6",
        border=f"1.5px solid {rx.color('gray', 5)}",
        background=rx.color("gray", 1),
        padding="28px",
        width="100%",
        max_width="400px",
        justify="center",
        border_radius="0.5rem",
    )





def feature_item(text: str) -> rx.Component:
    return rx.hstack(
        rx.icon("check", color=rx.color("accent", 9)),
        rx.text(text, size="4"),
    )


def features() -> rx.Component:
    return rx.vstack(
        feature_item("Feature No. 1"),
        feature_item("Feature No. 2"),
        feature_item("Feature No. 3"),
        feature_item("Feature No. 4"),
        feature_item("Feature No. 5"),
        width="100%",
        align_items="start",
    )


