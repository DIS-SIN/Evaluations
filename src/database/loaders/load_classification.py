from flask import Flask
CLASSIFICATIONS = [
    "AC",
    "AG",
    "AI",
    "AO",
    "AR",
    "AS",
    "AU",
    "BI",
    "CH",
    "CM",
    "CO",
    "CR",
    "CS",
    "CX",
    "DA",
    "DD",
    "DE","DS",
    "EC",
    "ED",
    "EG",
    "EL","EN",
    "EU",
    "FB",
    "FI",
    "FO",
    "FR",
    "FS",
    "GL",
    "GS",
    "GT",
    "HP",
    "HR",
    "HS",
    "IS",
    "LA",
    "LI",
    "LS",
    "MA",
    "MD",
    "MT",
    "ND",
    "NU",
    "OE",
    "OP",
    "PC",
    "PG",
    "PH",
    "PI",
    "PM",
    "PR(NS)",
    "PR(S)",
    "PS",
    "PY",
    "RO",
    "SC",
    "SE",
    "SG-SRE",
    "SG-PAT",
    "SO",
    "SRC",
    "SR(E)",
    "SR(W)",
    "ST",
    "SW",
    "TI",
    "TR",
    "UT",
    "VM",
    "WP"
]

def load_classifications(app: Flask):
    with app.app_context():
        from src.database import get_db
        from src.models.classification_model import ClassificationModel
        session = get_db()

        for cl in CLASSIFICATIONS:
            clobj = ClassificationModel(
                classification = cl
            )
            session.add(clobj)
        session.commit()