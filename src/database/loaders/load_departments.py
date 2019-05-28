from typing import cast
from flask import Flask
import os
import json

def load_departments(app: Flask):
    with app.app_context():
        from src.database import get_db
        from src.models.departments_model import DepartmentModel
        static_folder = cast(str,app.static_folder) 
        eng_data_path = os.path.join(
            static_folder, "data", "departments_en.json"
        )
        fr_data_path = os.path.join(
            static_folder, "data", "departments_fr.json"
        )

        with open(eng_data_path, encoding = "utf-8") as f:
            eng_data = json.loads(f.read(), encoding="utf-8")
        
        with open(fr_data_path, encoding = "utf-8") as f:
            fr_data = json.loads(f.read(), encoding="utf-8")
        
        session = get_db()

        for dept in eng_data:
            deptobj = DepartmentModel(
                department = dept,
                language="en"
            )
            if eng_data[dept]['abbreviation'] != "null":
                deptobj.abbreviation = eng_data[dept]['abbreviation']
            session.add(deptobj)
        
        for dept in fr_data:
            deptobj = DepartmentModel(
                department = dept,
                language="fr" 
            )
            if fr_data[dept]['abbreviation'] != "null":
                deptobj.abbreviation = fr_data[dept]['abbreviation']
            session.add(deptobj)
        
        session.commit()
        

