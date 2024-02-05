import pytest
import db
from app import app
import os
from utilities import (config)

@pytest.fixture(scope='module')
def api_app():
    return app

@pytest.fixture(scope='module')
def api_db():
    return db

#module scope enable share the test session between test functions
@pytest.fixture(scope='module')
def test_client(api_app, api_db):
    # flask_testing_app = create_new_client  # Assuming you have a testing config

    # Create a test client using the Flask application configured for testing
    with api_app.test_client() as testing_client:
        # Establish an application context before running the tests.
        with api_app.app_context():
            #db.create_all()  # Create all tables for the test DB
            yield testing_client  # this is where the testing happens!
            # db.swcdb.user.remove_all_users()
            api_db.swcdb.questions.remove_all_feedbacks()  # Clean up the DB after tests are done