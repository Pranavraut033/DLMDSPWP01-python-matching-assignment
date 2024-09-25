import pandas as pd
from bokeh.io import output_file
from bokeh.plotting import figure, show

from utils.Config import Config
from utils.FileHandler import FileHandler
from utils.IdealFunctionModel import IdealFunctionModel
from utils.sqlalchemy_helper import (
    IdealFunctions,
    TestData,
    TrainingData,
    create_tables,
    get_engine,
    get_session,
    load_ideal_functions,
    load_test_data,
    load_training_data,
)

config = Config.get_instance()


def load_data(session):
    """
    Loads training data, ideal functions, and test data into the session using file paths from configuration.
    """
    load_training_data(session, FileHandler(config.training_data_path))
    load_ideal_functions(session, FileHandler(config.ideal_functions_path))
    load_test_data(session, FileHandler(config.test_data_path))


def visualize(model):
    """
    Visualizes training data, ideal functions, and test data using Bokeh.
    """
    training_data = model.session.query(TrainingData).all()
    ideal_functions = model.session.query(IdealFunctions).all()
    test_data = model.session.query(TestData).all()

    # Convert to DataFrame for easier handling with Bokeh
    training_df = pd.DataFrame(
        [(d.id, d.x, d.y1, d.y2, d.y3, d.y4) for d in training_data],
        columns=["id", "x", "y1", "y2", "y3", "y4"],
    )
    ideal_df = pd.DataFrame(
        [
            (d.id, d.x) + tuple(getattr(d, f"y{i}") for i in range(1, 51))
            for d in ideal_functions
        ],
        columns=["id", "x"] + [f"y{i}" for i in range(1, 51)],
    )
    test_df = pd.DataFrame(
        [(d.id, d.x, d.y, d.delta_y, d.ideal_function) for d in test_data],
        columns=["id", "x", "y", "delta_y", "ideal_function"],
    )

    # Visualization
    p = figure(title="Training vs Ideal Functions", x_axis_label="x", y_axis_label="y")
    colors = ["red", "green", "blue", "orange", "purple", "brown", "pink"]

    # Plot training data
    for i in range(1, 5):
        p.scatter(
            training_df["x"],
            training_df[f"y{i}"],
            legend_label=f"Training y{i}",
            color=colors[i - 1],
            size=6,
            alpha=0.6,
        )

    # Plot ideal functions
    for i, func in enumerate(model.chosen_functions):
        p.line(
            ideal_df["x"],
            ideal_df[func],
            legend_label=f"Ideal {func}",
            color=colors[i],
            line_width=2,
        )

    # Plot test data
    p.scatter(
        test_df["x"],
        test_df["y"],
        legend_label="Test Data",
        color="black",
        size=6,
        marker="x",
    )

    p.legend.location = "top_left"

    output_file("main.html")
    show(p)


def visualize_ideal_function_with_test_data(model):
    """
    Fetches test data and ideal functions from the database, converts them to pandas DataFrames, and creates a Bokeh scatter plot.
    Plots test data points in black, and ideal functions in different colors.
    Outputs 'test_data_ideal_functions.html'.
    """

    # Fetch test data and corresponding ideal functions from the database
    test_data = model.session.query(TestData).all()
    ideal_functions = model.session.query(IdealFunctions).all()

    # Convert to DataFrame
    test_df = pd.DataFrame(
        [(td.x, td.y, td.delta_y, td.ideal_function) for td in test_data],
        columns=["x", "y", "delta_y", "ideal_function"],
    )
    ideal_df = pd.DataFrame(
        [
            (id_func.x,) + tuple(getattr(id_func, f"y{i}") for i in range(1, 51))
            for id_func in ideal_functions
        ],
        columns=["x"] + [f"y{i}" for i in range(1, 51)],
    )

    # Visualization
    p = figure(title="Test Data vs Ideal Functions", x_axis_label="x", y_axis_label="y")

    # Plot test data points
    p.scatter(
        test_df["x"],
        test_df["y"],
        legend_label="Test Data",
        color="black",
        size=6,
        marker="x",
    )

    colors = ["red", "green", "blue", "orange", "purple", "brown", "pink"]

    # Plot corresponding ideal functions
    for index, row in test_df.iterrows():
        ideal_func_col = row.ideal_function
        ideal_func_df = ideal_df[ideal_df["x"] == row["x"]]
        if not ideal_func_df.empty:
            p.scatter(
                ideal_func_df["x"],
                ideal_func_df[ideal_func_col],
                color=colors[model.chosen_functions.index(ideal_func_col)],
                size=6,
                legend_label=f"Ideal Function {row.ideal_function}",
            )

    p.legend.location = "top_left"

    output_file("test_data_ideal_functions.html")
    show(p)


def main():
    """
    Main function to execute the data processing and visualization pipeline.
    """
    # Initialize the database engine
    engine = get_engine(config.database_uri)
    # Create a new session for interacting with the database
    session = get_session(engine)
    # Create necessary tables in the database
    create_tables(engine)
    # Load data into the database
    load_data(session)
    # Initialize the model with the current session
    model = IdealFunctionModel(session)
    # Select ideal functions using the model
    model.select_ideal_functions()
    # Process test data with the model
    model.process_test_data()
    # Visualize the results of the model
    visualize(model)
    # Visualize the ideal functions along with the test data
    visualize_ideal_function_with_test_data(model)


if __name__ == "__main__":
    main()
