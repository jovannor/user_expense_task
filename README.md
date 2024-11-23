### Project Setup

To set up and run the project, follow these steps:

1. Clone the repository to your local machine.
2. Ensure that Docker Compose is installed.
3. Start the application by running the following command:

```bash
docker compose up -d
```
after  this actions you could open admin part by 
```bash
http://0.0.0.0:8000/admin 
```
use default credentioanals from default.env file
```bash
DEFAULT_ADMIN_EMAIL=admin@admin.com
DEFAULT_ADMIN_PASSWORD=qwerty123456!
```
Access the API documentation via Swagger or Redoc:

- Swagger: [http://0.0.0.0:8000/api/v0/swagger/](http://0.0.0.0:8000/api/v0/swagger/)
- Redoc: [http://0.0.0.0:8000/api/v0/redoc/](http://0.0.0.0:8000/api/v0/redoc/)

The documentation includes:
# API Endpoints Overview

## Users
- **GET** `/api/v0/users/`  
  Retrieve a list of all users with their transaction counts.

- **GET** `/api/v0/users/<user_id>/`  
  Retrieve details of a specific user.

- **GET** `/api/v0/users/<user_id>/transactions/`  
  Retrieve a user's transaction history (income and expenses).  
  **Filters:** `?date_min=YYYY-MM-DD&date_max=YYYY-MM-DD`

- **GET** `/api/v0/users/<user_id>/category-summary/`  
  Retrieve the total amount and count of expenses grouped by category.
  **Filters:**  
  - Categories: `?category=food,travel` `(food, travel, utilities, other)`
  - Dates: `?date_min=YYYY-MM-DD&date_max=YYYY-MM-DD`
    
## Transactions
###Expense
- **GET/POST** `/api/v0/users/<user_id>/expense/`  
  List or create an expense for a user.  
  **Filters:**  
  - Categories: `?category=food``(food, travel, utilities, other)`
  - Dates: `?date_min=YYYY-MM-DD&date_max=YYYY-MM-DD`

- **GET/PUT/DELETE** `/api/v0/users/<user_id>/expense/<expense_id>/`  
  Retrieve, update, or delete a specific expense.
###Income
- **GET/POST** `/api/v0/users/<user_id>/income/`  
  List or create an income for a user.  
  **Filters:**  
  - Card Types: `?card=visa` `(visa, mastercard)`
  - Dates: `?date_min=YYYY-MM-DD&date_max=YYYY-MM-DD`

- **GET/PUT/DELETE** `/api/v0/users/<user_id>/income/<income_id>/`  
  Retrieve, update, or delete a specific income.
