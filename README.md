# BlogVerse 🚀

A premium, feature-rich social blogging application built with **Django 6.0**, **Bootstrap 5**, and custom **Vanilla CSS**.

## ✨ Key Features

### 🌐 Social Network & Chat
- **Real-Time Messaging**: Built-in chat system with a **Floating Chat Box** and a full **Direct Message** page.
- **Message History**: Chat context is preserved, allowing you to load past conversations locally.
- **Friend System**: Send, accept, and manage friend requests.
- **User Search**: instant user lookup with auto-complete and search history context.
- **Notifications**: Real-time alerts for likes, comments, and friend requests.

### 🔐 Privacy & Authentication
- **Members Only**: Site content is restricted to registered users. Guests are redirected to a sleek Login/Register page.
- **Secure Authentication**: Built-in Django user management with real-time username availability checks.
- **Profile Customization**: Users get automatic profiles with image upload support and detailed bio/stats.

### 🎨 Visual Experience & Themes
- **Triple Theme Switcher**: 
    - 🎨 **Aesthetic**: A vibrant, modern gradient look.
    - 🌙 **Dark**: Midnight theme for low-light reading.
    - ☀️ **Light**: Clean, minimalist design.
- **Responsive Design**: Fully optimized for Mobile, Tablet, and Desktop with a mobile-first approach.
- **Premium Aesthetics**: Smooth transitions, glassmorphism elements, and modern typography.

### 📸 Rich Multimedia
- **Multiple Image Gallery**: Upload a main image + additional photos shown in a responsive carousel.
- **Short Video Support**: Upload and play MP4 videos directly within posts.
- **Interactive Feed**: Like and comment counts update in real-time.

### 💬 Advanced Interactivity
- **Smart Comments**: 
    - **5-Minute Edit Window**: Users can edit their typos shortly after posting.
    - **Moderation**: Post authors can delete any comment on their posts.
    - **Icon-Based Actions**: Sleek FontAwesome icons for Edit/Delete tasks.
- **AJAX Likes**: Heart posts instantly without page reloads.

### 📱 Connectivity & Hosting
- **Network Access**: Host the project on your local Wi-Fi to access it from any phone or tablet in your house.
- **Mobile First**: Redesigned feed and detail views for optimal viewing on small screens.
- **Chat Inbox 2.0**: A premium, mobile-responsive full-screen chat list with real-time search and unread indicators.

### 📍 Effortless Navigation
- **Smart Back Navigation**: Context-aware back buttons that return you to your exact previous state (e.g., search results).
- **Auto-Refresh Persistence**: Using JavaScript `pageshow` to ensure counts and content stay current when navigating back.
- **Sticky Headers**: Important actions always accessible.

## 🛠️ Installation & Setup

1. **Clone & Navigate**:
   ```bash
   cd project
   ```

2. **Virtual Environment**:
   ```bash
   python -m venv venv
   # Activate (Windows)
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Populate Content**:
   ```bash
   # Create Categories
   python populate_categories.py
   # Create Full Blog Content with AI Images
   python populate_full_blog.py
   ```

## 🌐 Hosting on Render (Public Deployment)

To host your blog permanently for the whole world to see:

1.  **Preparation**: I have already configured `settings.py` for WhiteNoise and added a `Procfile`.
2.  **Connect GitHub**: Go to [Render.com](https://render.com/) and create a free account.
3.  **Create Web Service**:
    *   Click **New +** -> **Web Service**.
    *   Connect your `blogverse-django` repository.
4.  **Settings**:
    *   **Build Command**: `pip install -r requirements.txt; python manage.py migrate; python manage.py collectstatic --noinput`
    *   **Start Command**: `gunicorn blog_project.wsgi`
5.  **Environment Variables**:
    *   Add `SECRET_KEY`: (Pick a random long string).
    *   Add `DEBUG`: `False`.

Render will automatically provide you with a public URL like `https://blogverse-xxxx.onrender.com`.

## 🌐 Hosting on Other Devices (Mobile/Tab)

To see your blog on your phone or another laptop:

1. **Get your Local IP**:
   Run `ipconfig` in CMD. Look for `IPv4 Address` (e.g., `192.168.x.x`).

2. **Run Server for Network**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

3. **Access**:
   On your phone's browser, go to `http://YOUR_IP:8000`.

## 📖 Documentation Guides
For more detailed information, refer to these custom guides:
- [**Full Project Blueprint**](blogging_project_sk.md): Contains the complete logic and code for every feature implemented.
- [**Command Quick-Start**](all_command.md): A simple, step-by-step list of commands for new device setup.

## 🚀 Usage

### Run Locally
```bash
python manage.py runserver
```
Access at: `http://127.0.0.1:8000/`

### Admin Credentials
- **Username:** `admin`
- **Password:** `admin`

## 📂 Project Highlights
- **`blog_app/`**: Core logic with custom model properties and permission-based views.
- **`chat/`**: Robust real-time messaging, friendship system, and premium inbox UI.
- **`users/`**: Advanced user management, profiles, and notifications.
- **`static/css/style.css`**: Refactored with CSS Variables and Mobile-Responsive media queries.
- **`templates/base.html`**: Host to the theme switcher and auto-refresh JavaScript.

## 🛠️ Troubleshooting
- **Site can't be reached?**: 
    1. Ensure both devices are on the SAME Wi-Fi.
    2. Check **Windows Firewall**: Allow `python.exe` through Private and Public networks.
    3. Use the IP address, not `127.0.0.1`, on other devices.
- **Post title showing code?**: This is caused by split template tags. Ensure `{{ post.title }}` is on a single line in your HTML.
- **Images missing?**: Run `python populate_full_blog.py` to generate the `media/` folder content.

---
*Developed  ❤️ by shubham yadav*
