from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

from utils.FileHandler import FileHandler

Base = declarative_base()


class TrainingData(Base):
    __tablename__ = "training_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float)
    y1 = Column(Float)
    y2 = Column(Float)
    y3 = Column(Float)
    y4 = Column(Float)


class IdealFunctions(Base):
    __tablename__ = "ideal_functions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float)
    # Dynamically create columns for ideal functions
    for i in range(1, 51):
        exec(f"y{i} = Column(Float)")


class TestData(Base):
    __tablename__ = "test_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float)
    y = Column(Float)
    delta_y = Column(Float, nullable=True, default=None)
    ideal_function = Column(String, nullable=True, default=None)


def get_engine(uri):
    return create_engine(uri)


def create_tables(engine):
    Base.metadata.create_all(engine)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def fetch_training_data(session):
    return session.query(TrainingData).all()


def fetch_ideal_functions(session):
    return session.query(IdealFunctions).all()


def fetch_test_data(session):
    return session.query(TestData).all()


def load_training_data(session, dataHandler: FileHandler) -> None:
    for _, row in dataHandler.data.iterrows():
        record = TrainingData(
            id=None,
            x=row["x"],
            y1=row["y1"],
            y2=row["y2"],
            y3=row["y3"],
            y4=row["y4"],
        )
        session.add(record)
    session.commit()


def load_ideal_functions(session: Session, dataHandler: FileHandler) -> None:
    for _, row in dataHandler.data.iterrows():
        record = IdealFunctions(
            id=None, x=row["x"], **{f"y{i}": row[f"y{i}"] for i in range(1, 51)}
        )
        session.add(record)
    session.commit()


def load_test_data(session, dataHandler: FileHandler) -> None:
    for _, row in dataHandler.data.iterrows():
        record = TestData(
            id=None,
            x=row["x"],
            y=row["y"],
            delta_y=row.get("delta_y", None),
            ideal_function=row.get("ideal_function", None),
        )
        session.add(record)
    session.commit()
