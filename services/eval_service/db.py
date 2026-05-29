"""Eval results persistence."""

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from eval_service.settings import settings


class Base(DeclarativeBase):
    pass


class EvalResult(Base):
    __tablename__ = "eval_results"

    id = Column(String, primary_key=True)
    run_id = Column(String, index=True)
    model_version = Column(String)
    system_mode = Column(String)
    metric_name = Column(String)
    score = Column(Float)
    judge_model = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)


def save_result(
    run_id: str,
    model_version: str,
    system_mode: str,
    metric_name: str,
    score: float,
    judge_model: str,
) -> None:
    import uuid

    with SessionLocal() as session:
        session.add(
            EvalResult(
                id=str(uuid.uuid4()),
                run_id=run_id,
                model_version=model_version,
                system_mode=system_mode,
                metric_name=metric_name,
                score=score,
                judge_model=judge_model,
            )
        )
        session.commit()
