# calculation/state.py
import reflex as rx
import pandas as pd
import io
import csv
from typing import Optional, List
from sqlalchemy import or_, cast, String

import reflex_local_auth.auth_session
from ..models import LoadModel, ProjectModel, UserInfo
from ..auth.state import SessionState
from sqlmodel import select, delete
from ..project.state import ProjectState


# Define the state class for loading the load entries
class LoadTableState(ProjectState):
    loads: List[LoadModel] = []
    #load: Optional['LoadModel'] = None

    search_value =""

    def load_loads(self, *args, **kwargs):
        #print("Projects's ID", self.project.id)
        #print ("Users Userinfo ID", self.my_userinfo_id)
        lookups = (
            (LoadModel.project_id == self.proj_id)
            #(UserInfo.user_id == self.my_userinfo_id)
        )
        with rx.session() as session:
            result = session.exec(
                select(LoadModel).where(lookups)
            ).all()
            self.loads = result
            #print (result)
            



    def get_load_detail(self):
        if self.proj_id is None:
            self.load = None
            return 
        lookups = (
            (LoadModel.project_id == self.proj_id)
        )
        with rx.session() as session:
            if self.proj_id == "":
                self.load = None
                return
            sql_statement = select(LoadModel).where(lookups)
            result = session.exec(sql_statement).one_or_none()
            self.load = result            
            #print(result)
            return self.load
    
    @rx.event
    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries()
        #print (self.search_value)


    @rx.event
    def load_entries(self) -> list[LoadModel]:
        # Start with your base query including the initial filters
        with rx.session() as session:
            lookups = (
                (LoadModel.project_id == self.proj_id) and
                (UserInfo.user_id == self.my_userinfo_id)
            )
            query = select(LoadModel).where(lookups)

            # Add search filters if search value exists
            if self.search_value != "":
                search_value = (
                    f"%{self.search_value.lower()}%"
                )
                query = query.where(
                    or_(
                        LoadModel.equip_id.ilike(search_value),
                        LoadModel.desc.ilike(search_value),
                        cast(LoadModel.power_kW, String).ilike(search_value),
                        cast(LoadModel.pf, String).ilike(search_value),
                        cast(LoadModel.eff, String).ilike(search_value),
                        cast(LoadModel.voltage, String).ilike(search_value),
                        LoadModel.u_equip_id.ilike(search_value),
                    )
                )
            self.loads = session.exec(query).all()


    def _convert_to_csv(self) -> str:
        """Convert the users data to CSV format."""

        # Make sure to load the entries first
        if not self.loads:
            self.load_entries()

        # Define the CSV file header excluding id and project_id
        fieldnames = [field for field in list(LoadModel.__fields__) 
            if field not in ["id", "project_id"]]

        # Create a string buffer to hold the CSV data
        output = io.StringIO()
        writer = csv.DictWriter(
            output, fieldnames=fieldnames
        )
        writer.writeheader()


        for load in self.loads:
            # Convert to dict and remove unwanted fields
            load_dict = load.dict()
            for field in ["id", "project_id"]:
                load_dict.pop(field, None)
            writer.writerow(load_dict)
        
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
                        # Modify the delete query to only use LoadModel
                        delete_query = delete(LoadModel).where(
                            LoadModel.project_id == self.proj_id
                        )
                        session.exec(delete_query)

                        # Add new entries
                        loads = []
                        csv_reader = csv.DictReader(io.StringIO(upload_data.decode()))
                        
                        for row in csv_reader:
                            try:
                                # Convert and validate data types
                                processed_row = {
                                    "equip_id": str(row["equip_id"]),
                                    "desc": str(row["desc"]),
                                    "voltage": float(row["voltage"]),
                                    "u_equip_id": str(row["u_equip_id"]),
                                    "power_kW": float(row["power_kW"]),
                                    "pf": float(row["pf"]),
                                    "eff": float(row["eff"]),
                                    "project_id": self.proj_id
                                }
                                
                                load = LoadModel(**processed_row)
                                loads.append(load)
                                
                            except (ValueError, KeyError) as e:
                                return rx.window_alert(
                                    f"Error processing row: {row}. Error: {str(e)}"
                                )
                        
                        # Bulk insert all processed rows
                        session.add_all(loads)
                        session.commit()
                        
                        # Refresh the objects to get the auto-generated IDs
                        for load in loads:
                            session.refresh(load)
                            
                    except Exception as db_error:
                        session.rollback()
                        return rx.window_alert(
                            f"Database error: {str(db_error)}"
                        )
                    
                # Refresh the table data after successful upload
                self.load_entries()
                return rx.window_alert("CSV file uploaded successfully!")
                
            except Exception as file_error:
                return rx.window_alert(
                    f"Error processing file: {str(file_error)}"
                )