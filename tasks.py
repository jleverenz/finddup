# invoke tasks

from invoke import task, run

@task
def test(ctx):
    ctx.run("python -m unittest discover tests/", pty=True)
    ctx.run("pep8 finddup/ tests/", pty=True)

@task
def html(ctx, live=False):
    if live:
        ctx.run("sphinx-autobuild . _build/html -r \".git/.*\"", pty=True)
    else:
        ctx.run("sphinx-build -M html . _build", pty=True)
