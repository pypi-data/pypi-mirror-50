import nox

@nox.session
def test_interactive(session):
    print(session.interactive)