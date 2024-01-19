import requests
import pandas as pd
import io
from .utils import custom_print
from db.utils import engine, session
from db.Incident import Casualty, Incident, Location, Time
from sqlalchemy.sql import text as sa_text


class ParseData:
    def __init__(
        self,
    ) -> None:
        self.data: pd.DataFrame = None
        self.incidents_df: pd.DataFrame = None
        self.casualties_df: pd.DataFrame = None
        self.times_df: pd.DataFrame = None
        self.locations_df: pd.DataFrame = None

        self.types = {
            "incidents": {
                "id": "string",
                "call_number": "string",
                "station_area": "category",
                "first_unit_on_scene": "category",
                "primary_situation": "category",
                "action_taken_primary": "category",
                "action_taken_secondary": "category",
                "action_taken_other": "category",
                "detector_alerted_occupants": "category",
                "property_use": "category",
                "area_of_fire_origin": "category",
                "ignition_cause": "category",
                "ignition_factor_primary": "category",
                "ignition_factor_secondary": "category",
                "heat_source": "category",
                "item_first_ignited": "category",
                "human_factors_associated_with_ignition": "category",
                "structure_type": "category",
                "structure_status": "category",
                "fire_spread": "category",
                "detectors_present": "category",
                "detector_type": "category",
                "detector_operation": "category",
                "detector_effectiveness": "category",
                "detector_failure_reason": "category",
                "automatic_extinguishing_sytem_type": "category",
            },
            "battalions": {
                "battalion": "category",
            },
            "times": {
                "incident_date": "datetime64[ns]",
                "alarm_dttm": "datetime64[ns]",
                "arrival_dttm": "datetime64[ns]",
                "close_dttm": "datetime64[ns]",
            },
            "casualties": {
                "fire_fatalities": int,
                "fire_injuries": int,
                "civilian_fatalities": int,
                "civilian_injuries": int,
            },
            "locations": {
                "address": "string",
                "city": "string",
                "zipcode": "string",
                "supervisor_district": float,
                "neighborhood_district": "string",
                "point": object,
            },
        }

    @staticmethod
    def fill_na_values(df: pd.DataFrame) -> pd.DataFrame:
        _df = df.copy()
        for col in _df.columns.values:
            _df_t = _df[col].dtype
            if _df_t == int or _df_t == "int64" or _df_t == float:
                _df[col] = _df[col].fillna(0)
            else:
                _df[col] = _df[col].fillna("-")

        return _df

    def extract_data(self) -> pd.DataFrame:
        url = "https://data.sfgov.org/resource/wr8u-xric.json"

        custom_print("Fetching data from", url)

        urlData = requests.get(url).content
        self.data = pd.read_json(io.StringIO(urlData.decode("utf-8")))
        custom_print("data already fetch")

        return self.data

    def transform_data(self):
        self.parse_extracted_data()

        custom_print("Filling empty values")
        self.incidents_df = self.fill_na_values(self.incidents_df)
        self.locations_df = self.fill_na_values(self.locations_df)
        self.times_df = self.fill_na_values(self.times_df)
        self.casualties_df = self.fill_na_values(self.casualties_df)

        custom_print("Parsing types")
        self.incidents_df = self.format_types(self.incidents_df, "incidents")
        self.locations_df = self.format_types(self.locations_df, "locations")
        self.times_df = self.format_types(self.times_df, "times")
        self.casualties_df = self.format_types(self.casualties_df, "casualties")

        # hot encode automatic_extinguishing_system_present to make it more understandable
        self.incidents_df["automatic_extinguishing_system_present"] = self.incidents_df[
            "automatic_extinguishing_system_present"
        ].map(lambda x: x == "1 -Present")

        self.locations_df["point"] = self.locations_df["point"].apply(lambda x: str(x))

    def format_types(self, df: pd.DataFrame, type: str) -> pd.DataFrame:
        return df.astype(self.types[type])

    def parse_extracted_data(self):
        custom_print("Formating data")
        time_dimension_columns = [
            "incident_date",
            "alarm_dttm",
            "arrival_dttm",
            "close_dttm",
        ]

        identification_columns = ["id"]

        casualties_dimension_columns = [
            "fire_fatalities",
            "fire_injuries",
            "civilian_fatalities",
            "civilian_injuries",
        ]

        battalion_dimension_columns = ["battalion"]

        location_dimension_columns = [
            "address",
            "city",
            "zipcode",
            "supervisor_district",
            "neighborhood_district",
            "point",
        ]

        new_columns = [
            col
            for col in self.data.columns.values
            if col not in location_dimension_columns
            and col not in time_dimension_columns
            and col not in casualties_dimension_columns
            and col not in battalion_dimension_columns
        ]

        # Foreign keys assigna

        location_dimension_columns += identification_columns
        time_dimension_columns += identification_columns
        casualties_dimension_columns += identification_columns
        battalion_dimension_columns += identification_columns

        self.incidents_df = self.data[new_columns]
        self.locations_df = self.data[location_dimension_columns]
        self.times_df = self.data[time_dimension_columns]
        self.casualties_df = self.data[casualties_dimension_columns]
        self.battalions_df = self.data[battalion_dimension_columns]

        self.locations_df = self.locations_df.rename(columns={"id": "incident_id"})
        self.times_df = self.times_df.rename(columns={"id": "incident_id"})
        self.casualties_df = self.casualties_df.rename(columns={"id": "incident_id"})
        self.battalions_df = self.battalions_df.rename(columns={"id": "incident_id"})

        custom_print("Incomming data already splited and formated")

    def load_data(self):
        custom_print(
            "saving data into wharehouse",
        )

        session.query(Location).delete()
        session.query(Casualty).delete()
        session.query(Time).delete()
        session.query(Incident).delete()
        session.commit()

        self.incidents_df.to_sql(
            "incidents_FT", engine, if_exists="append", index=False
        )
        self.locations_df.to_sql(
            "locations_DM", engine, if_exists="append", index=False
        )
        self.times_df.to_sql("times_DM", engine, if_exists="append", index=False)
        self.battalions_df.to_sql(
            "battalions_DM", engine, if_exists="append", index=False
        )
        self.casualties_df.to_sql(
            "casualties_DM", engine, if_exists="append", index=False
        )

        custom_print("data already saved into wharehouse")
