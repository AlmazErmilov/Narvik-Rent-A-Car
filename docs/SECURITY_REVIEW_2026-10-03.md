# Security review 2026-10-03

The deprecated Flask website was reviewed from `origin/main` at `4a9b5c9`. The current booking application lives in `poroshinaleksei/rent-car-client`. This change does not activate or deploy the deprecated website.

## Findings and changes

| Severity | Finding | Evidence and resolution |
| --- | --- | --- |
| High | Interactive debugger enabled in executable entry points | `rent_a_car_website/app.py` and `run.py` passed `debug=True`. Both now disable debug and bind the development server to loopback. ASVS 13.4.2. |
| Medium | Vulnerable Flask release | Full dependency resolution with pip-audit identified one unique Flask advisory, PYSEC-2026-2151. Flask is pinned to 3.1.3 and Flask-Babel to 4.0.0. The subsequent resolved scan has no known vulnerabilities in 10 packages. |
| Medium | Embedded signing key fallback | `config.py` had a fixed fallback. Configuration now reads only `SECRET_KEY` from the environment. This read-only site has no authentication or session-dependent forms, so no signing key is required for its existing routes. ASVS 13.3.1. |
| Low | Missing browser response protections | Responses now include nosniff, frame denial, referrer policy and a scoped CSP for framing, base URLs and object embedding. This is not a full script CSP. |
| Low | Broken alternate entry point and duplicate Babel initialization | `run.py` referred to a nonexistent factory. It now imports the existing app. Babel initialization occurs once and all six public pages still render. |

Jinja autoescaping is retained. The inspected site routes expose read-only content and do not accept booking or customer writes. No unsafe HTML rendering or direct SQL operation was found in these routes.

## Validation

- `python -m pytest tests -q`: 8 passed.
- `pip-audit -r rent_a_car_website/requirements.txt -f json`: resolved 10 packages, no known vulnerabilities.
- TruffleHog scanned the Git history on `main` with credential verification disabled. No detector findings. This does not establish absence of arbitrary passwords or prove credential validity.
- No production requests, database writes or cloud configuration changes were performed.

Security references: [Flask security guidance](https://flask.palletsprojects.com/en/stable/web-security/) and [Flask debugging guidance](https://flask.palletsprojects.com/en/stable/debugging/).

## Remaining limits

This deprecated repository should remain separate from the current production booking flow. Repository history and deployment inventory may contain material outside the reviewed Flask application. Development servers are not production hosting. Dependency scan results are a snapshot and need repeated checks over time.
