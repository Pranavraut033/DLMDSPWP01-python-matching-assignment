import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from utils.IdealFunctionModel import IdealFunctionModel, IdealFunctionError
from utils.sqlalchemy_helper import IdealFunctions, TestData, TrainingData


@pytest.fixture
def session():
    return MagicMock(spec=Session)


@pytest.fixture
def model(session):
    return IdealFunctionModel(session)


def least_square_deviation(y_true, y_pred):
    # Ensure arrays are the same length
    if len(y_true) != len(y_pred):
        raise ValueError("Input lists must have the same length")

    least_square_deviation = 0.0
    for yt, yp in zip(y_true, y_pred):
        least_square_deviation += (yt - yp) ** 2

    return least_square_deviation


def test_calculate_least_square_deviation(model):
    y_true = [1.0, 2.0, 3.0]
    y_pred = [1.1, 1.9, 3.2]
    result = model.calculate_least_square_deviation(y_true, y_pred)
    print(least_square_deviation(y_true, y_pred))
    assert result == pytest.approx(least_square_deviation(y_true, y_pred))


def test_select_ideal_functions(model, session):
    training_data = [
        TrainingData(x=1.0, y1=1.0, y2=2.0),
        TrainingData(x=2.0, y1=1.1, y2=2.1),
    ]
    ideal_functions = [
        IdealFunctions(x=1.0, y1=1.0, y2=2.0, y3=3.0, y4=4.0),
        IdealFunctions(x=2.0, y1=1.1, y2=2.1, y3=3.1, y4=4.1),
    ]
    session.query(TrainingData).all.return_value = training_data
    session.query(IdealFunctions).all.return_value = ideal_functions

    model.select_ideal_functions(ifunc_cols=4, td_cols=2)
    assert model.chosen_functions == ["y1", "y2"]


def test_select_ideal_functions_error(model, session):
    session.query(TrainingData).all.side_effect = Exception("Database error")
    with pytest.raises(
        IdealFunctionError, match="Error selecting ideal functions: Database error"
    ):
        model.select_ideal_functions()


def test_process_test_data(model, session):
    test_data = [
        TestData(x=1.0, y=1.05),
        TestData(x=2.0, y=2.05),
    ]
    ideal_functions = [
        IdealFunctions(x=1.0, y1=1.0, y2=2.0, y3=3.0, y4=4.0),
        IdealFunctions(x=2.0, y1=1.1, y2=2.1, y3=3.1, y4=4.1),
    ]
    session.query(TestData).all.return_value = test_data
    session.query(IdealFunctions).filter.return_value.first.side_effect = (
        ideal_functions
    )
    model.chosen_functions = ["y1", "y2", "y3", "y4"]

    model.process_test_data()

    assert test_data[0].delta_y == pytest.approx(0.05)
    assert test_data[0].ideal_function == "y1"
    assert test_data[1].delta_y == pytest.approx(0.05)
    assert test_data[1].ideal_function == "y2"
    session.commit.assert_called_once()
