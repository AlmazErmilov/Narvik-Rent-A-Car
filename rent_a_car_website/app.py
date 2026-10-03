from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
app.config.update(DEBUG=False, MAX_CONTENT_LENGTH=1024 * 1024)
babel = Babel()

app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['LANGUAGES'] = ['en', 'no', 'ru']

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

babel.init_app(app, locale_selector=get_locale)

@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = "frame-ancestors 'none'; base-uri 'self'; object-src 'none'"
    return response

@app.context_processor
def inject_get_locale():
    return dict(get_locale=get_locale)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/renting-agreement')
def renting_agreement():
    return render_template('renting_agreement.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/company-cars')
def company_cars():
    return render_template('company_cars.html')

if __name__ == '__main__':
    # ASVS 13.4.2: the interactive debugger must not be exposed.
    app.run(debug=False, host='127.0.0.1')

