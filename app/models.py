from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True)
    pollster = Column(String, index=True)
    race_id = Column(String, index=True)
    candidate = Column(String, index=True)
    party = Column(String, index=True)
    vote_share = Column(Float)
    sample_size = Column(Integer)
    field_date = Column(Date)
    source_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class HistoricalResult(Base):
    __tablename__ = "historical_results"

    id = Column(Integer, primary_key=True)
    pollster = Column(String, index=True)
    race_id = Column(String, index=True)
    candidate = Column(String)
    predicted_share = Column(Float)
    actual_share = Column(Float)


class PollsterGrade(Base):
    __tablename__ = "pollster_grades"

    id = Column(Integer, primary_key=True)
    pollster = Column(String, unique=True, index=True)
    mae = Column(Float)
    bias = Column(Float)
    reliability = Column(Float)
    composite_weight = Column(Float)


class FinanceRecord(Base):
    __tablename__ = "finance_records"

    id = Column(Integer, primary_key=True)
    candidate = Column(String, index=True)
    party = Column(String, index=True)
    receipts = Column(Float)
    disbursements = Column(Float)
    cash_on_hand = Column(Float)
    report_date = Column(Date)
    source_url = Column(String)


class RaceProjection(Base):
    __tablename__ = "race_projections"

    id = Column(Integer, primary_key=True)
    race_id = Column(String, index=True)
    candidate = Column(String, index=True)
    party = Column(String, index=True)
    win_probability = Column(Float)
    projected_share = Column(Float)


class DistrictMap(Base):
    __tablename__ = "district_maps"

    id = Column(Integer, primary_key=True)
    map_version = Column(String, index=True)
    district_id = Column(String, index=True)
    effective_date = Column(Date)
    previous_district_id = Column(String)
    weight_transfer = Column(Float, default=1.0)
