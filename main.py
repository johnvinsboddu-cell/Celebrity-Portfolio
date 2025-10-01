from application import create_app
# from self.models import Projects, Certifications, Skills, Work, Resume, Education
from user.models import User, Blocked
from admin.models import Celebrity
app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
