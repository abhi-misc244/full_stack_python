# calculation/state.py
import reflex as rx
import io
import csv
from typing import List
from sqlalchemy import or_, cast, String

from ...models import GeneratorModel, UserInfo
from sqlmodel import select, delete
from ...project.state import ProjectState


# Define the state class for loading the Generator entries
class GeneratorTableState(ProjectState):
    generators: List[GeneratorModel] = []
    search_value =""

    def load_generators(self, *args, **kwargs):
        lookups = (
            (GeneratorModel.project_id == self.proj_id)
        )
        with rx.session() as session:
            result = session.exec(
                select(GeneratorModel).where(lookups)
            ).all()
            self.generators = result
            



    def get_generator_detail(self):
        if self.proj_id is None:
            self.generator = None
            return 
        lookups = (
            (GeneratorModel.project_id == self.proj_id)
        )
        with rx.session() as session:
            if self.proj_id == "":
                self.generator = None
                return
            sql_statement = select(GeneratorModel).where(lookups)
            result = session.exec(sql_statement).one_or_none()
            self.generator = result            
            return self.generator
    
    @rx.event
    def filter_values(self, search_value):
        self.search_value = search_value
        self.generator_entries()


    @rx.event
    def generator_entries(self) -> list[GeneratorModel]:
        # Start with your base query including the initial filters
        with rx.session() as session:
            lookups = (
                (GeneratorModel.project_id == self.proj_id) and
                (UserInfo.user_id == self.my_userinfo_id)
            )
            query = select(GeneratorModel).where(lookups)

            # Add search filters if search value exists
            if self.search_value != "":
                search_value = (
                    f"%{self.search_value.lower()}%"
                )
                query = query.where(
                    or_(
                        GeneratorModel.equip_id.ilike(search_value),
                        GeneratorModel.desc.ilike(search_value),
                        cast(GeneratorModel.voltage, String).ilike(search_value),
                        GeneratorModel.scenario.ilike(search_value),
                        GeneratorModel.u_equip_id.ilike(search_value),
                    )
                )
            self.generators = session.exec(query).all()


    def _convert_to_csv(self) -> str:
        """Convert the users data to CSV format."""

        # Make sure to load the entries first
        if not self.generators:
            self.generator_entries()

        # Define the CSV file header excluding id and project_id and Swing Generator
        fieldnames = [field for field in list(GeneratorModel.__fields__) 
            if field not in ["id", "project_id", "swing_gen"]]

        # Create a string buffer to hold the CSV data
        output = io.StringIO()
        writer = csv.DictWriter(
            output, fieldnames=fieldnames
        )
        writer.writeheader()


        for generator in self.generators:
            # Convert to dict and remove unwanted fields
            generator_dict = generator.dict()
            for field in ["id", "project_id", "swing_gen"]:
                generator_dict.pop(field, None)
            writer.writerow(generator_dict)
        
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
                        # Modify the delete query to only use GeneratorModel
                        delete_query = delete(GeneratorModel).where(
                            GeneratorModel.project_id == self.proj_id
                        )
                        session.exec(delete_query)

                        # Add new entries
                        generators = []
                        csv_reader = csv.DictReader(io.StringIO(upload_data.decode()))
                        
                        for row in csv_reader:
                            try:
                                # Convert and validate data types
                                processed_row = {
                                    "equip_id": str(row["equip_id"]),
                                    "desc": str(row["desc"]),
                                    "power_kVA": float(row["power_kVA"]),
                                    "pf": float(row["pf"]),
                                    "voltage": float(row["voltage"]),
                                    "phase": int(row["phase"]),
                                    "u_equip_id": str(row["u_equip_id"]),
                                    "losses_per": float(row["losses_per"]),
                                    "scenario": str(row["scenario"]), 
                                    "project_id": self.proj_id,
                                    "swing_gen": False
                                }
                                
                                generator = GeneratorModel(**processed_row)
                                generators.append(generator)
                                
                            except (ValueError, KeyError) as e:
                                return rx.window_alert(
                                    f"Error processing row: {row}. Error: {str(e)}"
                                )
                        
                        # Bulk insert all processed rows
                        session.add_all(generators)
                        session.commit()
                        
                        # Refresh the objects to get the auto-generated IDs
                        for generator in generators:
                            session.refresh(generator)
                            
                    except Exception as db_error:
                        session.rollback()
                        return rx.window_alert(
                            f"Database error: {str(db_error)}"
                        )
                    
                # Refresh the table data after successful upload
                self.generator_entries()
                return rx.window_alert("CSV file uploaded successfully!")
                
            except Exception as file_error:
                return rx.window_alert(
                    f"Error processing file: {str(file_error)}"
                )
            
    @rx.var
    def select_generator(self) -> list[str]:
        with rx.session() as session:
            generators = session.exec(
                select(GeneratorModel)
            ).all()
            return [generator.equip_id for generator in generators]    


    @rx.event
    def update_gen_values(self, selected_eq_id: str):
        with rx.session() as session:
            # First set all generators' swing_gen to False and check pf
            generators = session.exec(
                select(GeneratorModel)
            ).all()
            
            for gen in generators:
                gen.swing_gen = False
                # Add error checking for pf
                if gen.pf is None and gen.equip_id != selected_eq_id:
                    gen.pf = 0.9
                session.add(gen)
                
            # Then set the selected generator's swing_gen to True
            generator = session.exec(
                select(GeneratorModel).where(GeneratorModel.equip_id == selected_eq_id)
            ).first()
            
            if generator:
                generator.swing_gen = True
                generator.pf = None
                session.add(generator)
                
            # Commit all changes at once
            session.commit()
            
        # Refresh the table data
        return self.generator_entries()





