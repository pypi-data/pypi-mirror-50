# Expand
This is a utility library to support expand testing in Nox. It provides
decorators to support parameterizing over the various libraries found
in a requirements.txt file. 

The goal is to allow the specification of a requirements.txt and expand
the version test to include the minimum version specified in the file
as well as any newer version of the package that are within the accepted
version range of the requirements specification.

The goal is to have the code be used in the following snippet:

```python
from expand import expander

@expander(requirements='requirements.txt')
@nox.session
def run_tests(session, expanded_pkgs):

    ...
    

    ...

    session.run('pytest')
