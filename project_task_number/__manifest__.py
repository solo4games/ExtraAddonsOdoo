{
    "name" : "Project Task sequence",
    "summary" : "Test case for project task using sequence",
    "version" : "14.0.0.0.1",
    "category" : "Project Task",
    "website": "https://cetmix.com",
    "author": "Cetmix",
    "license": "LGPL-3",
    "application": True,
    "installable": True,
    "depends":[
        "project"
    ],
    "data": [
        "data/sequence_data.xml",
        "views/project_task_number.xml"
    ],
    "demo": [
        
    ],
    'post_init_hook' : '_initialize_task_number'
}