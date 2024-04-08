python3 -m venv env

source env/bin/activate

cd SWARDEN/

python3 -m pip install -r requirements.txt

echo """from time import sleep
from os import environ, system, listdir
from os.path import isdir
from sys import argv


environ['DEBUG'] = 'True'
environ['ALLOWED_HOSTS'] = '*'
environ['DJANGO_SETTINGS_MODULE'] = 'CORE.settings.dev'

environ['EMAIL_HOST_USER'] = ''
environ['EMAIL_HOST_PASSWORD'] = ''

environ['CAPTCHA_TEST_MODE'] = 'True'


system('black -S .')
system('find -name "*.pyc" -type f -delete')
system('rm -rf `find -type d -name __pycache__`')


def run_false():
    system('python3 manage.py collectstatic --noinput')


def makemigrations():
    exclude_list = [
        'templates',
        'static',
        'CORE',
        'SWARDEN',
        'requirements',
        'staticfiles',
        'env',
        'media',
        'htmlcov',
    ]
    apps = [d for d in listdir('.') if isdir(d) and d not in exclude_list]
    system('python3 manage.py makemigrations ' + ' '.join(apps))


def migrate():
    system('python3 manage.py migrate')


def test():
    makemigrations()
    migrate()
    environ['DEBUG'] = 'False'
    system('python3 manage.py collectstatic --noinput')


def cleardb():
    system('rm -rf `find -type d -name migrations -not -path "./env/*"`')
    system('find -name "*.sqlite3" -type f -delete')
    exit(0)


def populatedb():
    makemigrations()
    migrate()
    system('python3 manage.py populateuser')
    system('python3 manage.py populatesecret')


def docker():
    system('docker compose -f docker-compose-dev.yml up')


def coverage():
    module = argv[2]
    omit_list = ['*/month/*', 'orchestrator.py', '*/migrations/*', 'manage.py']
    test()
    system(f'coverage run --source=\'{module}\' --omit=\'{",".join(omit_list)}\' manage.py test {module}')
    system('coverage html')


if argv[1] == 'runserver' and environ.get('DEBUG') == 'False':
    run_false()
elif argv[1] == 'makemigrations':
    makemigrations()
    exit()
elif argv[1] == 'test':
    test()
elif argv[1] == 'cleardb':
    cleardb()
elif argv[1] == 'populatedb':
    populatedb()
    exit()
elif argv[1] == 'docker':
    docker()
    system('python3 manage.py ' + ' '.join([i for i in argv[1:]]))
    exit()
elif argv[1] == 'coverage':
    coverage()
    exit()


sleep(3)
system('python3 manage.py ' + ' '.join([i for i in argv[1:]]))""" > orchestrator.py

python3 orchestrator.py populatedb
python3 orchestrator.py test
