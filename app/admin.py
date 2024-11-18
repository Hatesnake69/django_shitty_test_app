# admin.py
from django.contrib import admin, messages
from django import forms
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import WbTaskModel, WbOrderProductModel


class WbTaskForm(forms.ModelForm):
    class Meta:
        model = WbTaskModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['honest_sign_products'] = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


@admin.register(WbTaskModel)
class WbTaskModelAdmin(admin.ModelAdmin):
    list_display = ("employee", "account")
    form = WbTaskForm

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('save_product/', self.admin_site.admin_view(self.save_product), name='save_product'),
        ]
        return custom_urls + urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        task = WbTaskModel.objects.get(pk=object_id)
        products = WbOrderProductModel.objects.filter(order__supply__task=task, has_honest_sign=True)
        extra_context = extra_context or {}
        extra_context['products'] = products
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    @method_decorator(csrf_exempt)
    def save_product(self, request):
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            wb_sgtin = request.POST.get('wb_sgtin')
            try:
                product = WbOrderProductModel.objects.get(id=product_id)
                product.wb_sgtin = wb_sgtin
                product.save()
                return JsonResponse({'success': True, 'message': 'Изменения успешно сохранены.'})
            except WbOrderProductModel.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Продукт не найден.'})
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса.'})


@admin.register(WbOrderProductModel)
class WbOrderProductModelAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "code", "quantity", "wb_sgtin")
