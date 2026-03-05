from pytest_bdd import scenarios
from tests.bdd.steps.login_steps import *

# Load scenarios from feature file
scenarios('features/login.feature')
