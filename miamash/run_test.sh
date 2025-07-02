SINGLE_TEST_NAME="$1"
PREFIX="api.tests.RequestsReceiveTests"

python manage.py test "${PREFIX}.${SINGLE_TEST_NAME}"
