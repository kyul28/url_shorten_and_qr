# **URL Shortener API**

## **Project Overview**
This is a simple and efficient URL shortener built using **FastAPI** and **SQLite**. The application allows users to shorten long URLs, track click counts, generate QR codes, and set expiration dates for links.

---

## **Features**
- Shorten long URLs and generate unique short links.
- Track click statistics for shortened URLs.
- Set expiration dates for short links.
- Generate QR codes for easy link sharing.
- Admin panel to view and delete shortened URLs.
- Fast and lightweight with FastAPI and SQLite.

---

## **Technologies Used**
- **Backend:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Caching:** `functools.lru_cache`
- **QR Code Generation:** `qrcode`
- **Deployment:** Docker

---

## **Project Structure**

```
project_root/
│-- config.py          # Configuration settings
│-- crud.py            # Database operations
│-- database.py        # Database connection and session handling
│-- keygen.py          # URL key generation logic
│-- main.py            # API routes and application logic
│-- models.py          # Database schema definitions
│-- schemas.py         # Pydantic models for request/response validation
│-- requirements.txt   # Dependencies list
│-- .env               # Environment variables
│-- README.md          # Project documentation (this file)
```

---

## **Installation & Setup**

### **1. Prerequisites**
Make sure you have the following installed:

- Python 3.9+
- pip (Python package manager)
- SQLite (included with Python)
- Virtual environment (optional but recommended)

---

### **2. Clone the Repository**
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

---

### **3. Create and Activate Virtual Environment**
On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

---

### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

### **5. Configure Environment Variables**
Create a `.env` file in the project root and add:

```
ENV_NAME=Production
BASE_URL=http://localhost:8000
DB_URL=sqlite:///./shortener.db
DEFAULT_EXPIRATION_DAYS=7
```

---

### **6. Run the Application**
```bash
uvicorn main:app --reload
```

The application will run at:  
`http://localhost:8000`

---

## **API Endpoints**

### **1. Shorten a URL**
- **Endpoint:** `POST /url`
- **Request Body:**
  ```json
  {
    "target_url": "https://example.com",
    "target_key": "customkey",
    "expiration_days": 7
  }
  ```
- **Response:**
  ```json
  {
    "url": "http://localhost:8000/customkey",
    "admin_url": "http://localhost:8000/admin/customkey",
    "qr_url": "http://localhost:8000/qr/customkey"
  }
  ```

---

### **2. Redirect to Original URL**
- **Endpoint:** `GET /{url_key}`
- **Example:** `http://localhost:8000/customkey`
- **Response:** Redirects to original `target_url`

---

### **3. Retrieve URL Information**
- **Endpoint:** `GET /admin/{secret_key}`
- **Example Response:**
  ```json
  {
    "target_url": "https://example.com",
    "clicks": 42,
    "is_active": true,
    "expiration_date": "2025-02-01"
  }
  ```

---

### **4. Delete a Shortened URL**
- **Endpoint:** `DELETE /admin/{secret_key}`
- **Response:**
  ```json
  {
    "detail": "Successfully deleted shortened URL for 'https://example.com'!"
  }
  ```

---

### **5. Generate QR Code for Short URL**
- **Endpoint:** `GET /qr/{url_key}`
- **Example:** `http://localhost:8000/qr/customkey`
- **Response:** Returns a QR code image.

---

## **Running Tests**
To run tests and verify functionality, use:

```bash
pytest
```

---

## **Docker Setup (Optional)**
To run the application using Docker:

1. Build the Docker image:
   ```bash
   docker build -t url-shortener .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 url-shortener
   ```
3. Access the app at `http://localhost:8000`

---

## **Security Considerations**
- Ensure sensitive information is stored securely using environment variables.
- Implement API key authentication for production environments.
- Regularly update dependencies to mitigate vulnerabilities.

---

## **License**
This project is licensed under the MIT License. Feel free to use and modify it.
