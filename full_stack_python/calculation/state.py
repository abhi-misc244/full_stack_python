# calculation/state.py
import reflex as rx

class CalculationState(rx.State):
    result: str = None
    value1: int = 0
    value2: int = 0

    @classmethod
    def calculate(cls):
        cls.result = f"Result: {cls.value1 + cls.value2}"
        rx.update()
