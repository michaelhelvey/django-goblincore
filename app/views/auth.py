from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView


class LoginView(FormView):
    """
    Handle user login with email and password.
    """

    template_name = "auth/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")

    def get_success_url(self):
        if next := self.request.GET["next"]:
            return next
        return super().get_success_url()

    def dispatch(self, request, *args, **kwargs):
        # Redirect to home if already authenticated
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Log the user in
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass request to AuthenticationForm (required)
        kwargs["request"] = self.request
        return kwargs


def logout_view(request):
    """
    Log out the current user and redirect to login page.
    """
    logout(request)
    return redirect("login")
