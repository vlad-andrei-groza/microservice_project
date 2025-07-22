from prometheus_flask_exporter import PrometheusMetrics
from app import create_app
import os


app = create_app()

os.environ['DEBUG_METRICS'] = 'true'
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0')

if __name__ == "__main__":
    app.run(debug=True)
