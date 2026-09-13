from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False, 'message': getattr(error, 'description', 'Bad Request')}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'success': False, 'message': getattr(error, 'description', 'Unauthorized')}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'success': False, 'message': getattr(error, 'description', 'Forbidden')}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'message': getattr(error, 'description', 'Resource Not Found')}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'message': 'Internal Server Error occurred. Please try again later.'}), 500
