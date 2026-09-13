import sys
import os

# Dynamically add workspace root directory to sys.path so 'server' and 'ml' modules are always resolvable
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from server.app import create_app

env = os.getenv('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    print(f"KAIre Health REST API & ML Server starting on http://{host}:{port}")
    app.run(host=host, port=port, debug=(env == 'development'))

