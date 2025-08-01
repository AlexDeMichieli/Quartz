# 🖼️ Quartz - Online Photo Gallery

[![Python](https://img.shields.io/badge/Python-3.6.4+-3776ab?style=flat&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-3.0.3-092e20?style=flat&logo=django&logoColor=white)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-4.3-7952b3?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![Heroku](https://img.shields.io/badge/Deployed%20on-Heroku-430098?style=flat&logo=heroku&logoColor=white)](https://qwartz.herokuapp.com/)

Quartz is a modern, responsive online photo gallery built with Django. It allows users to create albums, upload images, and share their photo collections with a beautiful, intuitive interface.

**🚀 Live Demo:** [https://qwartz.herokuapp.com/](https://qwartz.herokuapp.com/)

## ✨ Features

- 📸 **Album Management** - Create and organize photo albums
- 🖼️ **Image Upload** - Upload multiple images with automatic optimization
- 👤 **User Authentication** - Secure user registration and login system
- 🔒 **Password Management** - Complete password reset functionality
- 📱 **Responsive Design** - Beautiful UI that works on all devices
- ☁️ **Cloud Storage** - Images stored on Amazon S3/Cloudinary for reliability
- 🎨 **Modern Interface** - Clean, intuitive design with Bootstrap 4

## 🛠️ Tech Stack

### Backend
- **Django 3.0.3** - Web framework
- **Python 3.6.4+** - Programming language
- **PostgreSQL** - Production database
- **SQLite** - Development database
- **Gunicorn** - WSGI HTTP Server

### Frontend
- **HTML5 & CSS3** - Markup and styling
- **Bootstrap 4.3** - CSS framework
- **JavaScript** - Interactive functionality
- **Responsive Design** - Mobile-first approach

### Cloud & Deployment
- **Heroku** - Platform as a Service
- **Amazon S3** - Image storage
- **Cloudinary** - Image processing and delivery
- **WhiteNoise** - Static file serving

### Key Libraries
- **Pillow** - Image processing
- **django-crispy-forms** - Enhanced form rendering
- **django-storages** - Cloud storage integration
- **sorl-thumbnail** - Thumbnail generation

## 🚀 Quick Start

### Prerequisites
- Python 3.6.4 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AlexDeMichieli/Quartz.git
   cd Quartz
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   NAME=your-db-name
   USER=your-db-user
   PASSWORD=your-db-password
   HOST=your-db-host
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser**
   Navigate to `http://127.0.0.1:8000/`

## 📖 Usage

### Creating Albums
1. Register for an account or log in
2. Navigate to the dashboard
3. Click "Create Album" 
4. Add a title and cover image
5. Start uploading your photos!

### Managing Photos
- Upload multiple images to any album
- View images in a beautiful gallery layout
- Delete albums and individual images
- Share your albums with others

### User Management
- Secure user registration and authentication
- Password change and reset functionality
- Personal dashboard for managing collections

## 🏗️ Project Structure

```
Quartz/
├── quartz_project/         # Main Django project settings
├── quartz_app/            # Core application (landing page)
├── library_app/           # Album and image management
├── users_app/             # User authentication
├── templates/             # HTML templates
├── static/               # Static files (CSS, JS, images)
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment configuration
├── runtime.txt          # Python version specification
└── manage.py           # Django management script
```

## 🚀 Deployment

The application is configured for easy deployment on Heroku:

1. **Create a Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   # Add other environment variables as needed
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

4. **Run migrations**
   ```bash
   heroku run python manage.py migrate
   ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Issues & Support

If you encounter any issues or have questions, please [open an issue](https://github.com/AlexDeMichieli/Quartz/issues) on GitHub.

---

## 😄 Fun Fact

**Why did the developer break up with their code?**

Because it wasn't returning their calls! 😄

---

<p align="center">Made with ❤️ by <a href="https://github.com/AlexDeMichieli">Alex De Michieli</a></p>
