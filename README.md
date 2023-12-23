# Django Orders Test Task

This is a Django test task for handling orders with Stripe integration.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) installed on your machine.

### Running the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/saltitc/django-orders.git
   cd django-orders
   ```

2. Create .env file by using .env-example template (preferred) and add the required environment variables:
    ```bash
    cp -f .env.example .env
    ```
3. Get the [Stripe API keys](https://dashboard.stripe.com/test/apikeys) and add to .env

4. Build and run the Docker container:
    ```bash
    docker-compose up --build
    ```
5. Go to http://localhost:8000