# Damn Vulnerable Blog (DVB)

Damn Vulnerable Blog (DVB) is a Flask-based blog web application intentionally designed to be vulnerable.

It provides common blogging features such as user registration, login, posting, commenting, changing passwords, and file uploads, but all implemented in insecure ways on purpose.

DVB is intentionally vulnerable to give you a hands-on learning experience in security testing. You can safely experiment with its flaws and study the source code to understand how vulnerabilities arise.

### ⚠️ **Disclaimer:**
- This project is for **educational and testing purposes only**.
-  I don't take any responsibility for misuse.
- Do **NOT** deploy it to production or expose it to the public internet.
- It is meant strictly for local or isolated environments such as VMs or containers.

---

## Security Flaws

This application includes these security flaws to explore and understand common web security issues:
- **SQL Injection (SQLi):**
	- Union-based SQL Injection
	- Authentication Bypass via SQL Injection
- **Cross-Site Scripting (XSS):**  
	- Reflected XSS  
	- Stored XSS  
	- DOM-based XSS  
- **Command Injection**
- **Server-Side Template Injection (SSTI)**
- **Path Traversal**
- **Insecure File Upload**
- **Cross-Site Request Forgery (CSRF)**
- **Server-Side Request Forgery (SSRF)**
- **Vulnerable Authentication Mechanism**  
- **Session Hijacking via Weak Secret Key**  
- **Insecure Direct Object Reference (IDOR)**
- **Broken Access Control in Unprotected admin functionality**

---

## Installation & Usage
1. Download the repository:
```bash
git clone https://github.com/Sec0gh/Damn-Vulnerable-Blog.git
cd Damn-Vulnerable-Blog
```

2. Install the requirements:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python3 app.py
```

4. Open the URL in your browser:
```
http://127.0.0.1:5000
```
---

## Configuration

All main settings are stored in `config.py`.  
You can modify them if you want to change how the application runs.

For example, to change the **IP address** or **Port**, edit the following lines in `config.py`:

```python
HOST = "127.0.0.1"
PORT = 5000
```
