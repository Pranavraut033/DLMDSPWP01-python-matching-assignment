# Python Assignment: Function Matching and Visualization

## Overview

This project is developed to match test data with ideal functions derived from training data sets using a least squares criterion. The process involves creating an SQLite database, loading the data, determining the best fit functions, and visualizing the results.

## Repository Structure

```bash
├── README.md
├── config.yaml
├── data.db
├── requirements.txt
└── src
    ├── data
    │   ├── ideal.csv
    │   ├── test.csv
    │   └── train.csv
    ├── main.html
    ├── main.py
    ├── tests
    │   ├── __init__.py
    │   ├── test_FileHandler.py
    │   └── test_IdealFunctionModel.py
    └── utils
        ├── Config.py
        ├── FileHandler.py
        ├── IdealFunctionModel.py
        ├── __init__.py
        └── sqlalchemy_helper.py
```

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_folder>
    ```

2. **Create and Activate Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The `config.yaml` file holds the configuration paths and database URI. Here is an example:

```yaml
database_uri: 'sqlite:///data.db'
training_data_path: 'src/data/train.csv'
ideal_functions_path: 'src/data/ideal.csv'
test_data_path: 'src/data/test.csv'
```

## Database Structure

The project uses an SQLite database with three tables to store training data, ideal functions, and test data.

### Training Data Table

| Column | Type  |
|--------|-------|
| id     | Integer (Primary Key, Auto-increment) |
| x      | Float |
| y1     | Float |
| y2     | Float |
| y3     | Float |
| y4     | Float |

### Ideal Functions Table

| Column | Type  |
|--------|-------|
| id     | Integer (Primary Key, Auto-increment) |
| x      | Float |
| y1     thru y50 | Float |
  
### Test Data Table

| Column         | Type    |
|----------------|---------|
| id             | Integer (Primary Key, Auto-increment) |
| x              | Float   |
| y              | Float   |
| delta_y        | Float (nullable, default=None) |
| ideal_function | Integer (nullable, default=None) |

## Usage

1. **Run the Main Program**
    ```bash
    python src/main.py
    ```

2. **Output**
    - A Bokeh visualization will be generated and can be accessed via the `main.html` file.
    - The results will be stored in the `data.db` SQLite database.

## Code Structure

### Main Modules

- `src/main.py`: The main entry point of the application which loads data, runs the function matching model, and visualizes the results.
- `src/utils/Config.py`: Handles configuration settings.
- `src/utils/FileHandler.py`: Handles file operations, specifically loading data from CSV files.
- `src/utils/IdealFunctionModel.py`: Contains the logic for selecting the ideal functions based on the least squares method.
- `src/utils/sqlalchemy_helper.py`: Manages database interactions using SQLAlchemy.

### Tests

Unit tests are located in the `src/tests` directory.

- `test_FileHandler.py`: Tests for the `FileHandler` class.
- `test_Model.py`: Tests for the `IdealFunctionModel` class.

Run the tests using:
```bash
pytest src/tests
```

## Example Workflow

1. **Load Training Data**
    - Training data from `train.csv` is loaded into the database.
   
2. **Load Ideal Functions**
    - Ideal functions from `ideal.csv` are loaded into the database.

3. **Load and Process Test Data**
    - Test data from `test.csv` is processed to match with the ideal functions.
    - Deviations are calculated and stored.

4. **Visualization**
    - Visualizations are created comparing the training functions, ideal functions, and test data.

## Git Workflow

1. **Clone the Develop Branch**
    ```bash
    git clone -b develop <repository_url>
    ```

2. **Add New Features**
    ```bash
    git add .
    git commit -m "Add new feature"
    git push origin develop
    ```

3. **Create a Pull Request**
    - A pull request should be created and reviewed before merging into the develop branch.

## Dependencies

- Python 3.x
- Pandas
- Numpy
- SQLAlchemy
- Matplotlib
- Bokeh
- Pytest
- PyYAML
- pytest-mock

## Contact

If you have any questions or need further assistance, please feel free to contact the maintainer.
