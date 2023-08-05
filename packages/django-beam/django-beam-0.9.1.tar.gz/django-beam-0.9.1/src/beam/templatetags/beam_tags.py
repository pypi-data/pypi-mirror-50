from django import template
from django.apps import apps
from django.db.models import Model, QuerySet, Manager, FieldDoesNotExist, ManyToManyRel
from django.db.models.fields.files import ImageFieldFile, FieldFile
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.template.loader import get_template
from django.urls import NoReverseMatch
from django.utils.http import urlencode
from typing import Dict, List, Tuple

from beam.layouts import layout_links
from beam.registry import get_viewset_for_model, default_registry
from beam.components import BaseComponent

register = template.Library()


@register.simple_tag
def get_link_url(component: BaseComponent, obj=None, **extra_kwargs):
    if not component:
        return None
    try:
        return component.reverse(obj, extra_kwargs)
    except NoReverseMatch:
        return None


@register.simple_tag
def get_attribute(obj, field):
    if getattr(field, "is_virtual", False):
        return field.get_value(obj)

    if not hasattr(obj, field):
        return None

    if hasattr(obj, "get_{}_display".format(field)):
        return getattr(obj, "get_{}_display".format(field))

    value = getattr(obj, field)

    if isinstance(value, Manager):
        return value.all()

    return value


@register.simple_tag
def get_form_field(form, field):
    try:
        return form[field]
    except KeyError:
        return None


@register.filter
def is_queryset(value):
    return isinstance(value, QuerySet)


@register.simple_tag(takes_context=True)
def get_url_for_related(context, instance, component_name):
    opts = get_options(instance)

    viewset = context.get("viewset", None)
    if viewset:
        registry = viewset.registry
    else:
        registry = default_registry

    try:
        viewset = get_viewset_for_model(registry, opts.model)
    except KeyError:
        return None

    return viewset().components[component_name].reverse(instance)


@register.filter
def is_image(model_field):
    return isinstance(model_field, ImageFieldFile)


@register.filter
def is_file(model_field):
    return isinstance(model_field, FieldFile)


@register.simple_tag
def get_options(instance_or_model):
    """
    Return the _meta options for a given model or instance.
    """
    if not instance_or_model:
        return None

    if isinstance(instance_or_model, Model):
        model = instance_or_model.__class__
    else:
        model = instance_or_model

    return model._meta


@register.filter
def field_verbose_name(instance, field):
    if hasattr(field, "verbose_name"):
        return field.verbose_name

    options = get_options(instance)

    try:
        model_field = options.get_field(field)
    except FieldDoesNotExist:
        model_field = None

    if hasattr(model_field, "verbose_name"):
        return model_field.verbose_name

    if isinstance(model_field, ForeignObjectRel):
        if model_field.multiple:
            return model_field.related_model._meta.verbose_name_plural
        else:
            return model_field.related_model._meta.verbose_name

    value = getattr(instance, field, None)
    return getattr(value, "verbose_name", field.replace("_", " "))


@register.simple_tag(takes_context=True)
def render_navigation(context):
    grouped = []
    for app_label, viewsets_dict in default_registry.items():
        group = {
            "app_label": app_label,
            "app_config": apps.get_app_config(app_label),
            "viewsets": viewsets_dict.values(),
        }
        grouped.append(group)
    navigation_template = get_template("beam/partials/navigation.html")
    request = context.get("request", None)
    return navigation_template.render({"apps": grouped, "request": request})


@register.simple_tag()
def fields_to_layout(fields):
    return [[fields]]


@register.simple_tag(takes_context=True)
def preserve_query_string(context, **kwargs):
    if not "request" in context:
        raise Exception(
            "The query_string tag requires django.core.context_processors.request"
        )
    request = context["request"]

    get = request.GET.copy()

    for item, value in kwargs.items():
        if value == "":
            get.pop(item, None)
        else:
            get[item] = value

    return "?{}".format(get.urlencode())


@register.simple_tag()
def get_visible_links(
    links: Dict[str, BaseComponent],
    link_layout: List[str],
    obj: Model = None,
    **extra_kwargs
) -> List[Tuple[BaseComponent, str]]:

    visible_links = []
    for link in layout_links(links, link_layout):
        try:
            url = link.reverse(obj, extra_kwargs=extra_kwargs)
        except NoReverseMatch:
            url = None

        if url:
            visible_links.append((link, url))
    return visible_links
