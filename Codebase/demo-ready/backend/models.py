from __future__ import annotations

from pydantic import BaseModel, Field, validator


class RouteRequest(BaseModel):
    start: list[float] = Field(..., description="Start coordinate [lng, lat]")
    end: list[float] = Field(..., description="End coordinate [lng, lat]")

    @validator("start", "end")
    def _validate_coord(cls, value: list[float]) -> list[float]:
        if len(value) != 2:
            raise ValueError("Coordinate must contain [lng, lat].")
        try:
            float(value[0])
            float(value[1])
        except (TypeError, ValueError) as exc:
            raise ValueError("Coordinate values must be numbers.") from exc
        return value
