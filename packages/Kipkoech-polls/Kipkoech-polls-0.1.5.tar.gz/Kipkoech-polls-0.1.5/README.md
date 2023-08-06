
KIPKOECH POLLS APP
==================
This is a simple Django polls app. It takes users inputs based on given choices and stores them in a Postgresql database. The results of the polls are then shown to the user.

[![CircleCI](https://circleci.com/gh/DenisBiwott/PollsApp/tree/master.svg?style=svg)](https://circleci.com/gh/DenisBiwott/PollsApp/tree/master)


Installation
------------

- Run 'fab deploy' to deploy the project. This runs the provision.yml playbook in the playbook folder which starts deployment using ansible.The provision.yml playbook imports deploy.yml which deploys the project to a AWS instance.
- The vars.yml playbook contains variables, hosts.yml contains hosts being deployed to, encrypt.yml makes the project hosted in HTTPS, supervisor.yml set up supervisor in the server, and continuous_dev.yml makes the project continually deployed in CIRCLECI.


Usage
-----

- The Kipkoech Polls project can be run locally via the command 'python3 manage.py runserver' or hosted using nginx and gunicorn. The first page is a page with poll questions. The user selects a questions and a list of options are displayed. The user selects an option and submits query (Click on the question and submit - there are no indications the question has been clicked). The user is then showed results page which gives results of the polls.

- The project is hosted on AWS and can be accessed using the domain [kipkoeck.cf]


Contributing
------------

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.


License
-------

[![License: MIT](https://img.shields.io/badge/License-MIT-neon.svg)](https://github.com/DenisBiwott/PollsApp/blob/master/LICENSE)
