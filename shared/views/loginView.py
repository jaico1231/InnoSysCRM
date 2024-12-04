from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from shared.loggin import log_event
from shared.forms.Autentication import AutenticationForm
from django.contrib.auth import logout

class LoginView(LoginView):
    template_name = 'login/login.html'
    form = AutenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context

def logout_view(request):
    log_event("usuario2", "LOGOUT", "El usuario ha cerrado sesión.")
    logout(request)    
    # Redirigir a la página de inicio u otra página después del logout
    return redirect('/login/')

    

