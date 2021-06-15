from django.views.generic import ListView , DetailView , CreateView, DeleteView , UpdateView 
from .models import Snack

class SnackListView(ListView):
    template_name = 'snack_list.html'
    model = Snack
    
class SnackDetailView(DetailView):
    template_name = 'snack_detail.html'
    model = Snack