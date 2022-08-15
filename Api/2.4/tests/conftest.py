from util.log import logger
import os, pytest


@pytest.fixture(autouse=True)
def auto_log():
    test_name = os.environ.get('PYTEST_CURRENT_TEST').split(' ')[0]
    logger.info(f"########start {test_name} ########")
    yield
    logger.info(f"########finish {test_name} ########")