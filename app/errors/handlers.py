from flask import render_template
from app import db
from app.errors import bp

# These handle common errors 

@bp.app_errorhandler(401)
def unauthorized_error(error):
    return render_template('errors/401.html'), 401

@bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(408)
def request_timeout_error(error):
    return render_template('errors/408.html'), 408

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@bp.app_errorhandler(502)
def bad_gateway_error(error):
    return render_template('errors/502.html'), 502

@bp.app_errorhandler(503)
def service_unavailable_error(error):
    return render_template('errors/503.html'), 503

@bp.app_errorhandler(504)
def gateway_timeout_error(error):
    return render_template('errors/504.html'), 504
