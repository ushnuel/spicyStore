from django.views import generic

class HomePage(generic.TemplateView):
    template_name = 'products/product_list.html'

class ThanksPage(generic.TemplateView):
    template_name = 'thanks.html'
