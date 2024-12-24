# calculation/state.py
import reflex as rx
import io
import csv
from typing import List
from sqlalchemy import or_, cast, String

from ...models import BusModel, UserInfo
from sqlmodel import select, delete
from ...project.state import ProjectState


# Define the state class for loading the Bus entries
class BusTableState(ProjectState):
    buses: List[BusModel] = []
    search_value =""

    def load_buses(self, *args, **kwargs):
        lookups = (
            (BusModel.project_id == self.proj_id)
        )
        with rx.session() as session:
            result = session.exec(
                select(BusModel).where(lookups)
            ).all()
            self.buses = result
            



    def get_bus_detail(self):
        if self.proj_id is None:
            self.bus = None
            return 
        lookups = (
            (BusModel.project_id == self.proj_id)
        )
        with rx.session() as session:
            if self.proj_id == "":
                self.bus = None
                return
            sql_statement = select(BusModel).where(lookups)
            result = session.exec(sql_statement).one_or_none()
            self.bus = result            
            return self.bus
    
    @rx.event
    def filter_values(self, search_value):
        self.search_value = search_value
        self.bus_entries()


    @rx.event
    def bus_entries(self) -> list[BusModel]:
        # Start with your base query including the initial filters
        with rx.session() as session:
            lookups = (
                (BusModel.project_id == self.proj_id) and
                (UserInfo.user_id == self.my_userinfo_id)
            )
            query = select(BusModel).where(lookups)

            # Add search filters if search value exists
            if self.search_value != "":
                search_value = (
                    f"%{self.search_value.lower()}%"
                )
                query = query.where(
                    or_(
                        BusModel.equip_id.ilike(search_value),
                        BusModel.desc.ilike(search_value),
                        cast(BusModel.voltage, String).ilike(search_value),
                        BusModel.scenario.ilike(search_value),
                        BusModel.u_equip_id.ilike(search_value),
                    )
                )
            self.buses = session.exec(query).all()


    def _convert_to_csv(self) -> str:
        """Convert the users data to CSV format."""

        # Make sure to load the entries first
        if not self.buses:
            self.bus_entries()

        # Define the CSV file header excluding id and project_id
        fieldnames = [field for field in list(BusModel.__fields__) 
            if field not in ["id", "project_id"]]

        # Create a string buffer to hold the CSV data
        output = io.StringIO()
        writer = csv.DictWriter(
            output, fieldnames=fieldnames
        )
        writer.writeheader()


        for bus in self.buses:
            # Convert to dict and remove unwanted fields
            bus_dict = bus.dict()
            for field in ["id", "project_id"]:
                bus_dict.pop(field, None)
            writer.writerow(bus_dict)
        
        # Get the CSV data as a string
        csv_data = output.getvalue()
        output.close()
        return csv_data
        


    @rx.event
    def download_csv_data(self):
        csv_data = self._convert_to_csv()
        return rx.download(
            data=csv_data,
            filename="data.csv",
        )
    

    @rx.event
    async def upload_csv(self, files: list[rx.UploadFile]):
        for file in files:
            try:
                # Read the upload data
                upload_data = await file.read()
                
                # Process the CSV data
                with rx.session() as session:
                    try:
                        # Modify the delete query to only use BusModel
                        delete_query = delete(BusModel).where(
                            BusModel.project_id == self.proj_id
                        )
                        session.exec(delete_query)

                        # Add new entries
                        buses = []
                        csv_reader = csv.DictReader(io.StringIO(upload_data.decode()))
                        
                        for row in csv_reader:
                            try:
                                # Convert and validate data types
                                processed_row = {
                                    "equip_id": str(row["equip_id"]),
                                    "desc": str(row["desc"]),
                                    "voltage": float(row["voltage"]),
                                    "phase": int(row["phase"]),
                                    "u_equip_id": str(row["u_equip_id"]),
                                    "losses_per": float(row["losses_per"]),
                                    "scenario": str(row["scenario"]), 
                                    "project_id": self.proj_id
                                }
                                
                                bus = BusModel(**processed_row)
                                buses.append(bus)
                                
                            except (ValueError, KeyError) as e:
                                return rx.window_alert(
                                    f"Error processing row: {row}. Error: {str(e)}"
                                )
                        
                        # Bulk insert all processed rows
                        session.add_all(buses)
                        session.commit()
                        
                        # Refresh the objects to get the auto-generated IDs
                        for bus in buses:
                            session.refresh(bus)
                            
                    except Exception as db_error:
                        session.rollback()
                        return rx.window_alert(
                            f"Database error: {str(db_error)}"
                        )
                    
                # Refresh the table data after successful upload
                self.bus_entries()
                return rx.window_alert("CSV file uploaded successfully!")
                
            except Exception as file_error:
                return rx.window_alert(
                    f"Error processing file: {str(file_error)}"
                )