# marshmallow-patch &ndash; A set of patches to the excellent [Marshmallow] library

[![][badge-python]][python-docs]
[![][badge-version]][repository-latest-release]

[![][badge-mit]][MIT License]
[![][badge-black]][Black]

[![][badge-ci-status]][repository-master]
[![][badge-ci-security]][repository-security]
[![][badge-codecov]][repository-codecov]

For | See
--- | ---
Documentation | https://psa-exe.gitlab.io/python-marshmallow-patch
Issue tracker | https://gitlab.com/psa-exe//python-marshmallow-patch/issues
Repository contents | [MANIFEST]
History of changes | [CHANGELOG]
Contribution/development guide | [CONTRIBUTING]
Copy of [MIT License] | [LICENSE]

---

## Installation

```bash
pip install pedroasad-marshmallow-patch
```

This library contains optional support for [Numpy] arrays and [Pint] physical units and quantities.
These may be installed by passing the `[numpy]`, `[pint]`, or `[all]` options when installing.

## Usage

It acts as a drop-in replacement to [Marshmallow]:

```python
from marshmallow_patch import marshmallow 
```

Further configuration may be performed by setting up global variables in [marshmallow_patch.config](https://psa-exe.gitlab.io/python-marshmallow-patch/api.html#module-marshmallow_patch.config) prior to importing the module replacement.
Other [Marshmallow] sub-modules may be imported directly from the original package.

---

*&mdash; Powered by [GitLab CI]*  
*&mdash; Created by Pedro Asad
[&lt;pasad@lcg.ufrj.br&gt;](mailto:pasad@lcg.ufrj.br) using [cookiecutter] and [@pedroasad.com/templates/python/python/app-1.0.0](https://gitlab.com/pedroasad.com/templates/python/python-app/tags/1.0.0)*  

[Black]: https://pypi.org/project/black/
[CHANGELOG]: ./CHANGELOG.md
[CONTRIBUTING]: ./CONTRIBUTING.md
[Gitlab CI]: https://docs.gitlab.com/ee/ci
[LICENSE]: ./LICENSE.txt
[MANIFEST]: ./MANIFEST.md
[MIT License]: https://opensource.org/licenses/MIT
[Numpy]: https://www.numpy.org/
[Pint]: https://pint.readthedocs.io/
[README]: https://gitlab.com/psa-exe//python-marshmallow-patch/blob/master/README.md
[TestPyPI]: https://test.pypi.org/
[badge-black]: https://img.shields.io/badge/code%20style-Black-black.svg
[badge-ci-coverage]: https://gitlab.com/psa-exe//python-marshmallow-patch/badges/master/coverage.svg
[badge-ci-security]: https://img.shields.io/badge/security-Check%20here!-yellow.svg
[badge-ci-status]: https://gitlab.com/psa-exe//python-marshmallow-patch/badges/master/pipeline.svg
[badge-codecov]: https://codecov.io/gl/psa-exe/python-marshmallow-patch/branch/master/graph/badge.svg
[badge-mit]: https://img.shields.io/badge/license-MIT-blue.svg
[badge-python]: https://img.shields.io/badge/Python-%E2%89%A53.6-blue.svg
[badge-version]: https://img.shields.io/badge/version-0.2.0%20alpha-orange.svg
[cookiecutter]: http://cookiecutter.readthedocs.io/
[Marshmallow]: https://marshmallow.readthedocs.io/en/3.0/
[python-docs]: https://docs.python.org/3.6
[repository-codecov]: https://codecov.io/gl/psa-exe/python-marshmallow-patch
[repository-latest-release]: https://test.pypi.org/project/marshmallow-patch/0.2.0/
[repository-master]: https://gitlab.com/psa-exe//python-marshmallow-patch
[repository]: https://gitlab.com/psa-exe//python-marshmallow-patch
[repository-security]: https://gitlab.com/psa-exe//python-marshmallow-patch/security

