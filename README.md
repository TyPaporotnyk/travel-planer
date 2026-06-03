# Travel Planner API

## Getting Started

### Environment Setup
Create a `.env` file in the root directory and configure it based on the provided template:
```bash
cp .env.dist .env
```

### Build and Run
Run the following command to build the Docker images and start all services in the background
```bash
docker compose up -d --build
```

## API Documentation
Once the application is running, the interactive Swagger documentation is available at:
```
http://127.0.0.1:8000/docs#/
```
