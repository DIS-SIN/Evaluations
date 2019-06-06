# TODO

* Create marshmallow schemas responsible for deserializing JSON from the API to sqlalchemy objects. Seperating the schemas for loading and dumping will reduce complexity and create a unidirectional data flow from the API to the database and back [IN PROGRESS]
* Complete sqlalchemy class definitions for the tables in the database
    * Survey Table: [DONE]
        * take out the logic to create a conducted survey from the model to the marshmallow loader [DONE]
        * create adjacency relationship such that relationships between surveys can be captured [DONE]
    * Conducted Survey Table:
        * Create hash for the conducted survey which only the respondant will have access to and so can reaccess the conducted survey if they wish to continue later (QR code ??) [DONE]
        * Add JSONB field for single level key value pairs for the results of the survey. (For dashboards) [DONE]
    * Conducted Question Table:
        * create field for the single level key value pair for the survey [DONE]
        * add many to one relationship between question and sections [DONE]
    * Sections Table:
        * Create Sections table which captures things like discriptions instructions ect [DONE]
        * Adjacency relationships between sections to implement subsection functionality
    
    *Section Type Table:
        * Capture all section types
            * matrix
            * ranking
            * group
            

    * Question Type Table:
        * capture all the question types
            * matrix_row
            * rank_row
            * mcq
            * dropdown
            * radio
            * text

* randomization of questions
* celery processes to calculate sentiment and prepare the single level key value pair for the conducted survey answers  
* query registhor for classifications, departments and offerings 
* API helper functions to reduce some bioler plate [DONE]
* From the classifications. get the base classification and the levels
* Integrate with sentry [DONE]
* allow the switching on or off of sentiment anlysis based on the availability of credentials DONE