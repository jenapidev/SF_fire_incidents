from __future__ import annotations
import datetime
from sqlalchemy.orm import relationship

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import json

from .utils import Base


class Incident(Base):
    __tablename__ = "incidents_FT"
    id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    incident_number: Mapped[int] = mapped_column(unique=True)
    exposure_number: Mapped[int] = mapped_column()
    call_number: Mapped[str] = mapped_column()
    battalion: Mapped[str] = mapped_column()
    station_area: Mapped[str] = mapped_column()
    suppression_units: Mapped[int] = mapped_column()
    suppression_personnel: Mapped[int] = mapped_column()
    ems_units: Mapped[int] = mapped_column()
    ems_personnel: Mapped[int] = mapped_column()
    other_units: Mapped[int] = mapped_column()
    other_personnel: Mapped[int] = mapped_column()
    first_unit_on_scene: Mapped[str] = mapped_column()
    number_of_alarms: Mapped[int] = mapped_column()
    primary_situation: Mapped[str] = mapped_column()
    mutual_aid: Mapped[str] = mapped_column()
    action_taken_primary: Mapped[str] = mapped_column()
    action_taken_secondary: Mapped[str] = mapped_column()
    action_taken_other: Mapped[str] = mapped_column()
    detector_alerted_occupants: Mapped[str] = mapped_column()
    property_use: Mapped[str] = mapped_column()
    estimated_contents_loss: Mapped[float] = mapped_column()
    area_of_fire_origin: Mapped[str] = mapped_column()
    ignition_cause: Mapped[str] = mapped_column()
    ignition_factor_primary: Mapped[str] = mapped_column()
    ignition_factor_secondary: Mapped[str] = mapped_column()
    heat_source: Mapped[str] = mapped_column()
    item_first_ignited: Mapped[str] = mapped_column()
    human_factors_associated_with_ignition: Mapped[str] = mapped_column()
    estimated_property_loss: Mapped[float] = mapped_column()
    structure_type: Mapped[str] = mapped_column()
    structure_status: Mapped[str] = mapped_column()
    floor_of_fire_origin: Mapped[float] = mapped_column()
    fire_spread: Mapped[str] = mapped_column()
    no_flame_spead: Mapped[float] = mapped_column()
    number_of_floors_with_minimum_damage: Mapped[float] = mapped_column()
    number_of_floors_with_significant_damage: Mapped[float] = mapped_column()
    number_of_floors_with_heavy_damage: Mapped[float] = mapped_column()
    number_of_floors_with_extreme_damage: Mapped[float] = mapped_column()
    detectors_present: Mapped[str] = mapped_column()
    detector_type: Mapped[str] = mapped_column()
    detector_operation: Mapped[str] = mapped_column()
    detector_effectiveness: Mapped[str] = mapped_column()
    detector_failure_reason: Mapped[str] = mapped_column()
    automatic_extinguishing_system_present: Mapped[bool] = mapped_column()
    automatic_extinguishing_sytem_type: Mapped[str] = mapped_column()
    automatic_extinguishing_sytem_perfomance: Mapped[str] = mapped_column()
    automatic_extinguishing_sytem_failure_reason: Mapped[str] = mapped_column()
    number_of_sprinkler_heads_operating: Mapped[float] = mapped_column()
    box: Mapped[float] = mapped_column()
    # relationships
    battalion: Mapped["Battalion"] = relationship(
        back_populates="incident",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    location: Mapped["Location"] = relationship(
        back_populates="incident",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    casualty: Mapped["Casualty"] = relationship(
        back_populates="incident",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    time: Mapped["Time"] = relationship(
        back_populates="incident",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Battalion(Base):
    __tablename__ = "battalions_DM"
    id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True)
    incident_id: Mapped[str] = mapped_column(
        ForeignKey("incidents_FT.id", ondelete="CASCADE")
    )
    battalion: Mapped[str] = mapped_column()
    incident: Mapped["Incident"] = relationship(back_populates="battalion")


class Casualty(Base):
    __tablename__ = "casualties_DM"
    id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True)
    incident_id: Mapped[str] = mapped_column(
        ForeignKey("incidents_FT.id", ondelete="CASCADE")
    )
    fire_fatalities: Mapped[int] = mapped_column()
    fire_injuries: Mapped[int] = mapped_column()
    civilian_fatalities: Mapped[int] = mapped_column()
    civilian_injuries: Mapped[int] = mapped_column()
    incident: Mapped["Incident"] = relationship(back_populates="casualty")


class Location(Base):
    __tablename__ = "locations_DM"
    id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True)
    incident_id: Mapped[str] = mapped_column(
        ForeignKey("incidents_FT.id", ondelete="CASCADE")
    )
    address: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    zipcode: Mapped[str] = mapped_column()
    supervisor_district: Mapped[float] = mapped_column()
    neighborhood_district: Mapped[str] = mapped_column()
    point: Mapped[str] = mapped_column()
    incident: Mapped["Incident"] = relationship(back_populates="location")

    def set_data(self, data):
        self.data = json.dumps(data)

    def get_data(self):
        return json.loads(self.data)


class Time(Base):
    __tablename__ = "times_DM"
    id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True)
    incident_id: Mapped[str] = mapped_column(
        ForeignKey("incidents_FT.id", ondelete="CASCADE")
    )
    incident_date: Mapped[datetime.datetime] = mapped_column()
    alarm_dttm: Mapped[datetime.datetime] = mapped_column()
    arrival_dttm: Mapped[datetime.datetime] = mapped_column()
    close_dttm: Mapped[datetime.datetime] = mapped_column()
    incident: Mapped["Incident"] = relationship(back_populates="time")
