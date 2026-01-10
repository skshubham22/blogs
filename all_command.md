# Commands to Run the Project on a New Device

Follow these steps in order to set up and run the blog project on another machine.

## 1. Environment Setup
Create and activate a virtual environment to keep dependencies isolated.

```bash
# Create the virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

## 2. Install Dependencies
Install all required libraries (Django, Pillow, Crispy Forms, etc.).

```bash
pip install -r requirements.txt
```

## 3. Database Preparation
Prepare the database and apply the existing structure.

```bash
python manage.py migrate
```

## 4. Administrative Access
Create an admin user to access the backend.

```bash
python manage.py createsuperuser
```

## 5. Run the Server
Starts the project for your local machine.

```bash
python manage.py runserver
```
**Access at:** `http://127.0.0.1:8000/`

---

## 6. Sharing with Other Devices (LAN)
If you want others on your Wi-Fi to see the site:

1. **Find your IP Address**:
   Type `ipconfig` (Windows) or `ifconfig` (Mac/Linux) and look for `IPv4 Address`.
2. **Run the server for the network**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
3. **Access from another device**:
   Open a browser on the other device and go to: `http://<YOUR_IP_ADDRESS>:8000`

---

### Admin Login
- **URL**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin`
