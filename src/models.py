"""
models.py - Modelos ORM para la base de datos del trading bot.
Soporta PostgreSQL (producción) y SQLite (desarrollo/testing).
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, JSON, Text,
    create_engine, Index,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def _defaultdict() -> Dict[str, Any]:
    return {}


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


class MarketData(Base):
    __tablename__ = "market_data"
    __table_args__ = (
        Index("ix_market_data_symbol_timestamp", "symbol", "timestamp"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    open: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    high: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    low: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    close: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    volume: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)


class Orderbook(Base):
    __tablename__ = "orderbook"
    __table_args__ = (
        Index("ix_orderbook_symbol_timestamp", "symbol", "timestamp"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    bids: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=_defaultdict)
    asks: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=_defaultdict)


class MarketTicker(Base):
    __tablename__ = "market_ticker"
    __table_args__ = (
        Index("ix_market_ticker_symbol_timestamp", "symbol", "timestamp"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    last_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    volume_24h: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    high_24h: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    low_24h: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)


class Trade(Base):
    __tablename__ = "trades"
    __table_args__ = (
        Index("ix_trades_symbol_outcome", "symbol", "outcome_status"),
        Index("ix_trades_timestamp_symbol", "timestamp", "symbol"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trade_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(10), nullable=False)
    order_id: Mapped[Optional[str]] = mapped_column(String(80), nullable=True, index=True)
    bybit_raw: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    entry_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    exit_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    tp_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sl_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    profit_loss: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    outcome_status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    outcome_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    decision: Mapped[str] = mapped_column(String(10), nullable=False)
    combined: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ild: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    egm: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    rol: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    pio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ogm: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    risk_reward_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=1.5)


class MetricSnapshot(Base):
    __tablename__ = "metric_snapshots"
    __table_args__ = (
        Index("ix_metric_snapshots_symbol_timestamp", "symbol", "timestamp"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    last_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    decision: Mapped[str] = mapped_column(String(10), nullable=False, default="hold")
    combined: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ild: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    egm: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    rol: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    pio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ogm: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    volatility: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    thresholds: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=_defaultdict)


class BalanceSnapshot(Base):
    __tablename__ = "balance_snapshots"
    __table_args__ = (
        Index("ix_balance_snapshots_timestamp", "timestamp"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    account_type: Mapped[str] = mapped_column(String(20), nullable=False, default="UNIFIED")
    coin: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    total_equity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    available_balance: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    raw: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=_defaultdict)


class ThresholdSnapshot(Base):
    __tablename__ = "threshold_snapshots"
    __table_args__ = (
        Index("ix_threshold_snapshots_timestamp", "timestamp"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    egm_buy_threshold: Mapped[float] = mapped_column(Float, nullable=False)
    egm_sell_threshold: Mapped[float] = mapped_column(Float, nullable=False)
    combined_buy_threshold: Mapped[float] = mapped_column(Float, nullable=False)
    combined_sell_threshold: Mapped[float] = mapped_column(Float, nullable=False)
    stats: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=_defaultdict)