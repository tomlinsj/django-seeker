from django.template import loader

from .mapping import Indexable, ModelIndex

import elasticsearch_dsl as dsl
import inspect
import logging
import threading


logger = logging.getLogger(__name__)


documents = []

model_documents = {}
model_doc_types = {}
app_documents = {}
app_field_templates = {}


def register(doc_class, app_label=None):
    assert issubclass(doc_class, Indexable)
    if doc_class in documents:
        logger.warning('Document class %s.%s was previously registered - skipping.', doc_class.__module__, doc_class.__name__)
        return
    documents.append(doc_class)
    if issubclass(doc_class, ModelIndex):
        model_class = doc_class.queryset().model
        # It's possible to register more than one document type for a model, so keep a list.
        model_documents.setdefault(model_class, []).append(doc_class)
        # For doing queries across multiple document types, we'll need a mapping from doc_type back to model_class.
        model_doc_types[doc_class._doc_type.name] = model_class
        app_field_templates[doc_class._doc_type.name] = {}
        for key, properties in doc_class._doc_type.mapping.properties._params.items():
            for field in properties:
                search_templates = []
                for cls in inspect.getmro(doc_class):
                    if issubclass(cls, dsl.DocType):
                        search_templates.append('seeker/%s/%s.html' % (cls._doc_type.name, field))
                search_templates.append('seeker/column.html')
                app_field_templates[doc_class._doc_type.name].update({field: {'search_templates': search_templates,
                                                                              'template_obj': loader.select_template(search_templates)}})
    if app_label:
        app_documents.setdefault(app_label, []).append(doc_class)
