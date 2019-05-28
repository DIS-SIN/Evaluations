from flask import Flask

def load_regions(app: Flask):
    with app.app_context():
        from src.database import get_db
        from src.models.regions_model import RegionModel
        session = get_db()

        west = RegionModel(
            language = "en",
            region = "west"
        )

        east = RegionModel(
            language = "en",
            region = "east"
        )
        
        central = RegionModel(
            language = "en",
            region = "central"
        )

        north = RegionModel(
            language = "en",
            region = "north"
        )

        ncr = RegionModel(
            language = "en",
            region = "ncr"
        )

        rcn = RegionModel(
            language = "fr",
            region = "rcn"
        )

        nord = RegionModel(
            language = "fr",
            region = "nord"
        )

        central = RegionModel(
            language = "fr",
            region = "central"
        )

        est = RegionModel(
            language = "fr",
            region = "est"
        )

        ouest = RegionModel(
            language = "fr",
            region = "ouest"
        )

        session.add(west)
        session.add(east)
        session.add(north)
        session.add(central)
        session.add(ncr)
        session.add(rcn)
        session.add(nord)
        session.add(est)
        session.add(ouest)
        session.add(central)
        session.commit()



