- Build Docker image :
    docker build -t relevanc:1.0 .

- Launch unit test :
    docker run -ti relevanc:1.0 unit_tests

- Launch script :
    docker run -v local/path/to/randomized-transactions-202009.psv:/relevanC/randomized-transactions-202009.psv -ti relevanc:1.0
