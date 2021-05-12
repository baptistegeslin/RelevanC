def task_run_isort():
    """ Sort Python imports """
    return {
        "actions": ["pipenv run isort ."],
    }


def task_unit_tests():
    """Launch Unit Tests with pytest"""
    return {
        "actions": ["pipenv run python -m pytest -v"],
        "task_dep": ["run_isort"],
        "verbosity": 2,
    }


def task_run_script():
    """Launch Unit Tests with pytest"""
    return {
        "params": [
            {"name": "code_path", "short": "c", "type": str, "default": "RelevanC", "help": "Path of the code of python"},
            
        ],
        "actions": ["pipenv run python -m package.code.__main__"],
        "verbosity": 2,
    }
