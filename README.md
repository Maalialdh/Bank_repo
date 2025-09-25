# Banking with Python🏦

## 📌 Overview
This project is a **Banking CLI application** written in Python.  
It simulates basic banking operations such as **account creation, login, deposit, withdraw, transfer, and saving data to CSV**.

## Technologies Used
- **Python 3.8+**  
- Built-in libraries: `csv`, `os`  
- Command-Line Interface (CLI)

## Application Functionality

| Feature | Description | Status |
|---------|------------|--------|
| Create new customer | Add a customer with optional checking or savings account | ✅ Done |
| Deposit money | Add funds to checking or savings accounts | ✅ Done |
| Withdraw money | Withdraw funds with overdraft handling | ✅ Done |
| Transfer money | Transfer funds between own accounts or another customer's account | ✅ Done |
| Login / Logout | Secure login system for customers | ✅ Done |
| View accounts | Display balances and account information | ✅ Done |
| Account deactivation | Automatically deactivate account after 2 overdrafts | ✅ Done |

---
## Challenges / Key Takeaways
- Handling **overdraft logic** and ensuring account status updates correctly was tricky.  
- Managing **multiple accounts per customer** required a flexible class structure.  
- Saving and loading data from CSV while keeping **overdraft count and account status** consistent required careful handling.  
- Learned how to **structure a CLI project** using proper classes (`Account`, `Customer`, `Bank_repo`) for maintainability.
---

## IceBox Features (Future Improvements)
- Password encryption for security  
- Interest calculation for savings accounts  
- Account statements / transaction history  
- GUI interface for easier interaction  
- Notifications for low balance or overdraft warnings  
