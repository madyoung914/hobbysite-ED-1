from django.views.generic.list import ListView
from user_management.models import Profile
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


class AppsListView(ListView):
    model = Profile
    template_name = 'main_interface/homepage.html'


class UserCreateView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = "main_interface/register.html"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = CreateUserForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            return super().form_valid(form)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy("user_management:profile")

'''
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = CreateUserForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CreateUserForm(request.POST)

        if form.is_valid():
            name = self.object.username

            user = User.objects.create_user
            login(request, user)

            transaction = form.save(commit=False)
            transaction.product = self.object
            transaction.buyer = request.user.profile

            if self.object.stock == 0:
                self.object.status = 'OOS'

            transaction.status = 'CART'

            transaction.save()
            self.object.save()

            return redirect(reverse('merchstore:merch-cart'))
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


'''