from fabric import task


def run(c, cmd):
    c.run(cmd, replace_env=False, echo=True)


@task
def freeze(c):
    run(c, "rm -f requirements.txt")
    run(c, "pipenv lock -r > requirements.txt")


@task
def format(c):
    run(c, "black .")
    run(c, "autoflake --remove-all-unused-imports -i -r .")
