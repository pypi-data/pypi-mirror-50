import os

try:
    from django.conf import settings
except ModuleNotFoundError:
    settings = None

# if an environment file exists, load it into the env.
# if django exists, load the variables from the django config over the environment variable.
if os.path.exists('environment.ini'):
    env_file = open('environment.ini')
    for line in env_file:
        trim_line = line.rstrip('\n').strip()
        if not trim_line or trim_line.startswith("#"):
            continue
        if "=" not in trim_line:
            print(f"Skipping invalid environment.ini variable: '{trim_line}'")
        variable, value = trim_line.split('=')
        os.environ[variable] = value


def get_django_var_or_env(variable_name):
    return getattr(
        settings,
        variable_name,
        os.environ.get(variable_name, None)
    )


def ultima_file_path(file_name):
    return os.path.join(ULTIMA_FILES_DIR, file_name)


ULTIMA_FILES_DIR = os.path.abspath(get_django_var_or_env('ULTIMA_FILES_DIR'))
