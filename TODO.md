# TODO

* Create marshmallow schemas responsible for deserializing JSON from the API to sqlalchemy objects. Seperating the schemas for loading and dumping will reduce complexity and create a unidirectional data flow from the API to the database and back
* Complete sqlalchemy class definitions for the tables in the database
    * Survey Table:
        * take out the logic to create a conducted survey from the model to the marshmallow loader
        * create adjacency relationship such that relationships between surveys can be captured
    * Conducted Survey Table:
        * Create hash for the conducted survey which only the respondant will have access to and so can reaccess the conducted survey if they wish to continue later (QR code ??)
        * Add JSONB field for single level key value pairs for the results of the survey. (For dashboards)
    * Conducted Question Table:
        * create field for the single level key value pair for the survey
        * create adjacency relationship such that relationships between questions can be captured i.e. parent question 
        * add many to one relationship between question and prequestion
    * PreQuestion Table:
        * Create PreQuestion table which captures things like discriptions instructions ect 
    * Question Type Table:
        * capture all the question types
            * matrix
            * matrix_row
            * mcq 
            * dropdown
            * radio
            * text
* randomization of questions
* celery processes to calculate sentiment and prepare the single level key value pair for the conducted survey answers  
* query registhor for classifications, departments and offerings 
* API helper functions to reduce some bioler plate    