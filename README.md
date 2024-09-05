

# Transaction Management API

This project is a Django REST framework application that provides an API for managing transactions, generating PDFs, and handling user authorization via JWT tokens. It uses PostgreSQL as the database backend.

## Features

- **POST** `/api/v1/transactions/create` - Create a new transaction
- **GET** `/api/v1/transactions/list` - List all transactions
- **GET** `/api/v1/transactions/:txnid` - Retrieve a specific transaction by ID
- **DELETE** `/api/v1/transactions/:txnid` - Delete a specific transaction by ID
- **PUT** `/api/v1/transactions/:txnid` - Update a specific transaction by ID
- **PATCH** `/api/v1/transactions/:txnid` - Partially update a specific transaction by ID
- **GET** `/api/v1/pdf/transactions/` - Download a PDF containing all transactions
- **GET** `/api/v1/pdf/transactions/:txnid` - Download a PDF containing a specific transaction's details

## Authentication

- **JWT Authentication** is used for secure API access.
  - **Staff Users**: Can POST, PATCH, PUT, and GET transactions.
  - **Manager Users**: Have access to all endpoints .

## Setup Instructions

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**

   Create a `.env` file in the root directory with the following contents:

   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=''
   DB_USER=''
   DB_PASSWORD=''
   DB_HOST=''
   DB_PORT=''
   ```

3. **Migrate the Database**

   Run migrations to set up your database schema:

   ```bash
   python manage.py migrate
   ```

4. **Run the Development Server**

   Start the Django development server:

   ```bash
   python manage.py runserver
   ```

5. **Swagger Documentation**

   Access the Swagger API documentation at:

   [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

   Swagger provides a user-friendly interface for exploring and interacting with the API endpoints.

## Endpoints and Example Requests

### Create a Transaction

- **POST** `/api/v1/transactions`

  **Request Body**:
  ```json
  {
    "name": "John Doe",
    "phone": "9865012345",
    "email": "johndoe@gmail.com",
    "amount": 10000.00,
    "transaction_date": "2023-12-30"
  }
  ```

  **Response**:
  ```json
  {
   "message": "Created successfully"
  }
  ```

### List Transactions

- **GET** `/api/v1/transactions`

  **Response**:
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": "TXNID91D995C95289",
        "name": "admin",
        "phone": "98274823",
        "email": "admin@gmial.com",
        "amount": "1334.00",
        "transaction_date": "2024-09-05T18:04:03.310781Z"
      }
   ]
  }
  ```

### Retrieve a Transaction

- **GET** `/api/v1/transactions/:txnid`

  **Response**:
  ```json
  {
    "txnid": "TXNID0057",
    "name": "John Doe",
    "phone": "9865012345",
    "email": "johndoe@gmail.com",
    "amount": 10000.00,
    "transaction_date": "2024-09-05T18:04:03.310781Z"
  }
  ```

### Update a Transaction

- **PUT** `/api/v1/transactions/:txnid`

  **Request Body**:
  ```json
  {
    "name": "John Doe",
    "phone": "9865012345",
    "email": "johndoe@gmail.com",
    "amount": 12000.00
  }
  ```

### Partially Update a Transaction

- **PATCH** `/api/v1/transactions/:txnid`

  **Request Body**:
  ```json
  {
    "amount": 12000.00
  }
  ```

### Delete a Transaction

- **DELETE** `/api/v1/transactions/:txnid`

### Generate PDF for All Transactions

- **GET** `/api/v1/pdf/transactions/`

### Generate PDF for a Specific Transaction

- **GET** `/api/v1/pdf/transactions/:txnid`

## Authorization Rules

- **Staff**:
  - Allowed to POST, PATCH, PUT, and GET transactions.
  - Cannot access PDF endpoints.

- **Manager**:
  - Allowed to perform all actions including accessing PDF endpoints.


## Example Authorization Header

Use the following format for sending JWT tokens in requests:

```
Authorization: Bearer <your_jwt_token>
```

Example:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1NjQyOTgyLCJpYXQiOjE3MjU1NTY1ODIsImp0aSI6ImVhMWVjYjc0NWZkZDQ4OTJiNzRlNGJhZjQ5YmExODA0IiwidXNlcl9pZCI6IjQwYjA4MWRmLTA3MDAtNDg5Yi1hZTJkLTRjODllOWM2OWE0YyJ9.wENiqZMaM3LANw2ihn43K4_wwNIwILOrh8UrdS_g3wI
```

**Recommended Modheader extension to add token**
  - https://modheader.com/

---

