# starnavi_test_task

The project relies on the following dependencies:

- **Python**: `^3.10`
- **Pre-commit**: `^3.7.0`
- **Flake8**: `^7.0.0`
- **Mypy**: `^1.9.0`
- **Isort**: `^5.13.2`
- **FastAPI**: `^0.110.1`
- **Uvicorn**: `^0.29.0`
- **Alembic**: `^1.13.1`
- **Pydantic**: `^2.6.4`
- **Networkx**: `^3.3`
- **Matplotlib**: `^3.8.4`
- **Asyncpg**: `^0.29.0`
- **Types-redis**: `^4.6.0.20240409`
- **FastAPI-Cache2**: `^0.2.1`
- **Psycopg2**: `^2.9.9`
- **Httpx**: `^0.27.0`
- **Pytest-asyncio**: `^0.23.6`

### To run the project with Docker Compose, execute the following command:

docker-compose up --build


OpenAPI docs: http://0.0.0.0:8000/docs

## Endpoints
### Workflow Endpoints
- **POST /workflows**
  - Creates a new workflow with the provided details.

- **PUT /workflows/{workflow_id}**
  - Updates an existing workflow identified by its ID.

- **DELETE /workflows/{workflow_id}**
  - Deletes an existing workflow identified by its ID.

- **GET /workflows/{workflow_id}**
  - Retrieve details of a specific workflow identified by its ID.

- **GET /workflows/{workflow_id}/draw**
  - Draws the graphical representation of a workflow identified by its ID.

### Edge Endpoints

- **POST /edges**
  - Creates a new edge between two nodes.

- **PUT /edges/{edge_id}**
  - Updates an existing edge identified by its ID.

- **DELETE /edges/{edge_id}**
  - Deletes an existing edge identified by its ID.

- **GET /edges/{edge_id}**
  - Retrieve details of a specific edge identified by its ID.

### Node Endpoints

- **POST /nodes**
  - Creates a new node with the provided details.

- **PUT /workflows/{node_id}**
  - Updates an existing node identified by its ID.

- **DELETE /workflows/{node_id}**
  - Deletes an existing node identified by its ID.

- **GET /workflows/{node_id}**
  - Retrieve details of a specific node identified by its ID.
