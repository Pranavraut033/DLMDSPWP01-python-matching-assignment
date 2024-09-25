from typing import List, Tuple

import numpy as np
from sqlalchemy.orm import Session

from utils.sqlalchemy_helper import IdealFunctions, TestData, TrainingData


class IdealFunctionError(Exception):
    pass


#
class IdealFunctionModel:
    """
    IdealFunctionModel selects ideal functions that best fit the training data based on the least square deviation.

    Attributes:
        session (Session): Database session for querying training data and ideal functions.
        chosen_functions (List[str]): List of chosen ideal function names.
    """

    def __init__(self, session: Session):
        self.session = session
        self.chosen_functions: List[str] = []

    def calculate_least_square_deviation(
        self, y_true: List[float], y_pred: List[float]
    ) -> float:
        """
        Calculate the least square deviation between the true and predicted values.
        """
        return np.sum((np.array(y_true) - np.array(y_pred)) ** 2)

    def select_ideal_functions(self, ifunc_cols=50, td_cols=4) -> None:
        """
        Selects the ideal functions that best fit the training data based on the least square deviation.

        Queries training data and ideal functions from the database, calculates least square deviation for each combination, and selects the ideal function with the minimum deviation for each training column. Selected ideal functions are stored in `chosen_functions`.
        """

        try:
            training_data = self.session.query(TrainingData).all()
            ideal_functions = self.session.query(IdealFunctions).all()
            training_y_columns: List[List[float]] = [
                [getattr(td, f"y{i+1}") for td in training_data] for i in range(td_cols)
            ]

            ideal_function_columns: List[List[float]] = [
                [getattr(ifunc, f"y{j+1}") for ifunc in ideal_functions]
                for j in range(ifunc_cols)
            ]
            print(training_y_columns)
            print(ideal_function_columns)
            for y_train in training_y_columns:
                deviations: List[Tuple[int, float]] = []

                for idx, y_ideal in enumerate(ideal_function_columns):
                    deviation = self.calculate_least_square_deviation(y_train, y_ideal)
                    print(
                        f"Deviation for y{idx+1}: {deviation}, y_train: {y_train}, y_ideal: {y_ideal}"
                    )
                    deviations.append((idx + 1, deviation))

                best_fit = min(deviations, key=lambda x: x[1])[0]
                self.chosen_functions.append(f"y{best_fit}")
        except Exception as e:
            raise IdealFunctionError(f"Error selecting ideal functions: {e}")

    def process_test_data(self) -> None:
        """
        Processes the test data, matches each test point to the best fitting ideal function, and calculates deviations.
        Queries test data from the database, matches each test point with the closest ideal function based on deviation, and stores the matched ideal function and deviation in the database.
        """
        test_data = self.session.query(TestData).all()

        for test_point in test_data:
            min_deviation = float("inf")
            best_function = None
            ideal_point = (
                self.session.query(IdealFunctions)
                .filter(IdealFunctions.x == test_point.x)
                .first()
            )

            if not ideal_point:
                print(f"Ideal point not found for x={test_point.x}")
                continue

            for idx, func in enumerate(self.chosen_functions):
                ideal_value = getattr(ideal_point, func)
                deviation = abs(test_point.y - ideal_value)

                if deviation < min_deviation:
                    min_deviation = deviation
                    best_function = self.chosen_functions[idx]

            test_point.delta_y = min_deviation
            test_point.ideal_function = best_function

        self.session.commit()
