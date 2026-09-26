from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    """Public lead form with a hidden honeypot."""

    website = forms.CharField(required=False, widget=forms.HiddenInput)
    form_type = forms.CharField(widget=forms.HiddenInput, required=False)
    source = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Lead
        fields = ("name", "phone", "telegram", "comment", "source", "form_type")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Имя", "autocomplete": "name"}),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Телефон",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                }
            ),
            "telegram": forms.TextInput(attrs={"placeholder": "Telegram (необязательно)"}),
            "comment": forms.Textarea(
                attrs={"placeholder": "Комментарий: техника, сроки, город", "rows": 4}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Имя"
        self.fields["phone"].label = "Телефон"
        self.fields["telegram"].label = "Telegram"
        self.fields["comment"].label = "Комментарий"
        self.fields["telegram"].required = False
        self.fields["comment"].required = False
        for name, field in self.fields.items():
            if name == "website":
                continue
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css} field-input".strip()

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("spam")
        return ""

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip()
        digits = [ch for ch in phone if ch.isdigit()]
        if len(digits) < 10:
            raise forms.ValidationError("Укажите телефон с кодом страны.")
        return phone
