from django import forms
from .models import Ticket

class ChatbotForm(forms.Form):
    hw_type = forms.ChoiceField(
        label='Hardware Type',
        choices=[],  # Choices will be set in the view
        required=True
    )
    apps_sw = forms.ChoiceField(
        label='Software/Application',
        choices=[],
        required=True
    )
    report_type = forms.ChoiceField(
        label='Report Type',
        choices=[],
        required=True
    )
    report_desc = forms.CharField(
        label='Problem Description',
        widget=forms.Textarea,
        required=True
    )
    pc_ip = forms.CharField(
        label='PC IP Address',
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(ChatbotForm, self).__init__(*args, **kwargs)
        self.fields['hw_type'].choices = self.get_distinct_choices('hw_type')
        self.fields['apps_sw'].choices = self.get_distinct_choices('apps_sw')
        self.fields['report_type'].choices = self.get_distinct_choices('report_type')

    def get_distinct_choices(self, field_name):
        distinct_values = Ticket.objects.values_list(field_name, flat=True).distinct()
        return [(value, value) for value in distinct_values if value]

