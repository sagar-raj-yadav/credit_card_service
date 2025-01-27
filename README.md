
### **1. Home Page**
- **URL:**  
  `https://credit-card-service.onrender.com/`
- **Method:**  
  `GET`


---

### **5. Trigger Billing Cron**
- **URL:**  
  `https://credit-card-service.onrender.com/api/trigger-billing-cron/`
- **Method:**  
  `GET`
  
---

### **2. Register User**
- **URL:**  
  `https://credit-card-service.onrender.com/api/register-user/`
- **Method:**  
  `POST`
- **Body:**  
  ```json
  {
    "name": "sagar raj yadav",
    "email": "sagaryadav@example.com",
    "aadhar_id": "123456789012",
    "phone": "9876543210",
    "address": "Bhopal"
  }
  ```

---

### **3. Apply for a Loan**
- **URL:**  
  `https://credit-card-service.onrender.com/api/apply-loan/`
- **Method:**  
  `POST`
- **Body:**  
  ```json
  {
    "user": 1,  // Replace 1 with the unique user ID from "register-user" response
    "amount": 50000,
    "loan_term": 12, 
    "interest_rate": 10.5
  }
  ```

---

### **4. Make Payment**
- **URL:**  
  `https://credit-card-service.onrender.com/api/make-payment/`
- **Method:**  
  `POST`
- **Body:**  
  ```json
  {
    "loan": 1,  // Replace 1 with the loan ID from "apply-loan" response
    "amount": 5000,
    "payment_date": "2025-01-27"
  }
  ```




---


