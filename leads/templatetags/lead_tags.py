from django import template

from leads.forms import LeadForm

register = template.Library()


@register.inclusion_tag("includes/lead_form.html", takes_context=True)
def lead_form(context, form_type="general", source="", title="", submit="Оставить заявку", compact=False, vehicle=None):
    request = context.get("request")
    initial_source = source
    if vehicle is not None:
        initial_source = vehicle.name
        form_type = form_type or "vehicle"
    return {
        "form": LeadForm(initial={"form_type": form_type, "source": initial_source}),
        "form_type": form_type,
        "source": initial_source,
        "title": title,
        "submit_label": submit,
        "compact": compact,
        "request": request,
        "next": request.get_full_path() if request else "/",
    }
