from .Login import LoginView
from ..forms import SignupForm


class SignupView(LoginView):
    """Signup view"""

    template_name = "users/signup.html"
    form_class = SignupForm
