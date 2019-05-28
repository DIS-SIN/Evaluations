from sqlalchemy.ext.declarative.api import DeclarativeMeta
import random

def generate_slug(suffix: str, model: DeclarativeMeta, session) -> str:
    slug_animals = [
    "alligator","ant",
    "bear",
    "bee",
    "bird","camel","cat","cheetah","chicken",
    "chimpanzee","cow","crocodile","deer","dog"
    ,"dolphin","duck","eagle","elephant","fish","fly"
    ,"fox","frog","giraffe","goat","goldfish","hamster",
    "hippopotamus","horse","kangaroo","kitten","lion","lobster","monkey",
    "octopus","owl","panda","pig","puppy","rabbit",
    "rat","scorpion","seal","shark","sheep","snail","snake","spider","squirrel","tiger",
    "turtle","wolf","zebra"
    ]
    slug_animals_len = len(slug_animals)
    slug_colours = [
    "black","blue","brown","gray","green","orange","pink","purple","red","white","yellow"
    ]
    slug_colours_len = len(slug_colours)
    slug_jobs = [
    "accountant","actor","actress","athlete","author","baker",
    "banker","barber","beautician","broker","burglar","butcher",
    "carpenter","chauffeur","chef","clerk","coach","craftsman",
    "criminal","crook","dentist","doctor","editor","engineer",
    "farmer","fire-fighter","fisherman","judge","lawyer","magician",
    "mechanic","musician","nurse","pharmacist","pilot","poet","policeman",
    "politician","printer","professor","rabbi","priest","pastor","sailor",
    "salesman","shoemaker","soldier","tailor","teacher","veterinarian","waiter",
    "waitress","watchmaker"
    ]
    slug_jobs_len = len(slug_jobs)
    unique = False
    while unique is False:
        colour = slug_colours[random.randint(0, slug_colours_len - 1)]
        animal_1 = slug_animals[random.randint(0, slug_animals_len - 1)]
        animal_2 = slug_animals[random.randint(0, slug_animals_len - 1)]
        job = slug_jobs[random.randint(0, slug_jobs_len - 1)]
        slug = "_".join([colour,animal_1,animal_2,job,suffix])
        row_with_slug = session.query(model).filter_by(slug=slug).one_or_none()
        if row_with_slug is None:
            unique = True
    return slug   