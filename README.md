# Microservice Python Project

A Python-based microservice for computing common mathematical operations 
(power, Fibonacci and factorial), with support for request logging via Kafka, 
Prometheus-based monitoring, REST API, and optional front-end interface.

--- 

## Features

- 📘 REST API using **Flask**
- 🧮 Supported operations:
  - `power(base, exponent)`
  - `fibonacci(n)`
  - `factorial(n)`
- 🪵 Logging via **Kafka Producer**
- 📊 Metrics exposure via **Prometheus**
- 🧾 Simple front-end (HTML, CSS + JS) for interaction

---

## 📁 Project Structure

```
microservice_project/
├── app/
│   ├── __init__.py          # app initialization
│   ├── api.py               # API endpoints
│   ├── db.py                # SQLAlchemy setup
│   ├── models.py            # DB models and Pydantic models
│   ├── operations.py        # Core math logic                   
│   ├── web.py               # Web UI blueprint
│   ├── services/
│   │   ├── logger.py                   # Kafka producer for logging
│   │   ├── consumer_service.py         # Kafka consumer for displaying logs
│   │   └── docker-compose.kafka.yml    # Docker Compose to run Kafka + ZooKeeper
│   ├── static/
│   │   ├── script.js        # JavaScript logic
│   │   └── styles.css       # webpage styles
│   ├── templates/
│   │   └── index.html       # HTML front-end
│── config.py                # Configuration settings
├── run.py                   # App entry point
│ 
└── README.md
```

---
## API Endpoints
This microservice provides a RESTful API for performing mathematical operations. 
Below is a summary of the available endpoints:

| Method | Endpoint              | Description                                                 |
|--------|-----------------------|-------------------------------------------------------------|
| GET    | `/`                   | index page of the front-end app                             |
| GET    | `/metrics`            | get request duration metrics and request counters by using PrometheusMetrics |
| POST   | `/api/math/pow`       | Compute power function                                      |
| POST   | `/api/math/fibonacci` | Compute Fibonacci                                           |
| POST   | `/api/math/factorial` | Compute factorial                                           |
| GET    | `/api/math/pow`       | Retrieve pow operations stored in the db                    |
| GET    | `/api/math/fibonacci` | Retrieve Fibonacci computations                             |
| GET    | `/api/math/factorial` | Retrieve factorial computations                             |

---
## Technical Details
### How a Factorial Request Works

### 1. Request Flow
Client sends a POST request to:
```bash
POST /api/math/factorial
Content-Type: application/json

{
  "n": 5
}
```

### 2. Request Validation
A Pydantic model is used to validate the request body:
```python
from pydantic import BaseModel, Field

class FactorialRequest(BaseModel):
    n: int = Field(..., ge=0)
```
If the input is invalid (e.g., a negative number), the route returns a 400 with a validation error.

### 3. Database Model – MathOperationRequest
Each operation is stored in the database via SQLAlchemy from flask_sqlalchemy
```python
class MathOperationRequest(db.Model):
    __tablename__ = 'math_operations'

    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(50), nullable=False)
    input = db.Column(db.String(50), nullable=False)
    result = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<MathOperationRequest {self.id} - {self.operation}({self.input}) = {self.result}>"
```

### 4. Computation
The actual computation of factorial is performed in the `operations.py` module:
```python
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

### 5. API Endpoint Implementation
Here is how the `/factorial` endpoint is defined in `api.py`:
```python
@math_operations_bp.route('/factorial', methods=['POST'])
def factorial_route():
    data = flask.request.get_json()
    parsed_data, errors = parse_request(FactorialRequest, data)
    if errors:
        return jsonify(errors=errors), 400
    result = factorial(parsed_data.n)
    store_request("factorial", f"n={parsed_data.n}", result)

    # Log the event
    log_event("factorial_operation", {
        "operation": "factorial",
        "input": f"n={parsed_data.n}",
        "result": result
    })

    return jsonify(ResultResponse(result=result).model_dump())
```
The endpoint receives a POST request with JSON data.
It validates the input using Pydantic, computes the factorial, 
stores the request in the database and logs the event via Kafka. 
Finally, it returns the result in JSON format.

### 6. Response
The response is also validated using Pydantic  to ensure it matches the expected format.
Results of the computations are integers or floats 
(when the exponent in power operation is a negative number):
```python
from pydantic import BaseModel

class ResultResponse(BaseModel):
    result: int | float
```

Response example:
```json
{
  "result": 120
}
```

## Web Client UI
- Accessible at: `http://localhost:5000/`
- Supports submitting requests via form inputs
- Shows results and displays errors using a snackbar

---

## Logging
- All API requests are logged via `KafkaProducer`
- Messages are published to topic: `math-operations-logs`
- A sample Kafka consumer is included to process messages (see `consumer_service.py`)

---

## Monitoring
- Prometheus-compatible metrics are exposed at `/metrics`
- Includes:
  - Total HTTP requests
  - Response codes per endpoint
  - Response duration
- Can be integrated with Prometheus and Grafana for dashboard visualization

