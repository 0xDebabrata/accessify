VIRTUAL_ENV_NAME=fast

if [[ command -v python3 >/dev/null 2>&1 ]]; then
    echo Python 3 is installed  # POSIX-compliant
fi 

echo Creating Virtual Environment : $VIRTUAL_ENV_NAME
python3 -m venv $VIRTUAL_ENV_NAME
source ./$VIRTUAL_ENV_NAME/bin/activate
pip install -r requirements.txt