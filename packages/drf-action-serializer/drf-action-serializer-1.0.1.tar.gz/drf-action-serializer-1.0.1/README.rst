Action Serializer
=================

.. image:: https://travis-ci.org/gregschmit/drf-action-serializer.svg?branch=master
    :target: https://travis-ci.org/gregschmit/drf-action-serializer

.. image:: https://img.shields.io/pypi/v/drf-action-serializer
    :alt: PyPI
    :target: https://pypi.org/project/drf-action-serializer/

.. image:: https://coveralls.io/repos/github/gregschmit/drf-action-serializer/badge.svg?branch=master
    :target: https://coveralls.io/github/gregschmit/drf-action-serializer?branch=master

Source: https://github.com/gregschmit/drf-action-serializer

PyPI: https://pypi.org/project/drf-action-serializer/

Action Serializer is a Django Rest Framework extension package that provides a
Serializer that implements per-action field configuration for use in your
drf-powered API.

**The Problem**: When building APIs, often you want different serializers for
different actions, such as less fields on a list view vs a detail view. Normally
you would have to build multiple Serializers to support this.

**The Solution**: This app provides the ``ModelActionSerializer`` which allows
you to easily configure per-action serialization.


How to Use
==========

.. code-block:: shell

    $ pip install drf-action-serializer

In your serializer, inherit from ``action_serializer.ModelActionSerializer``.

In your serializer, you can add an ``action_fields`` dictionary to the ``Meta``
class and use ``fields``, ``exclude``, and ``extra_kwargs`` under the action
key. The example in this project shows how to render a smaller list of
attributes for a list view compared to the detail view.

.. code-block:: python

    from django.contrib.auth.models import Group
    from .serializers import ModelActionSerializer


    class GroupActionSerializer(ModelActionSerializer):
        """
        An example serializer for the Django ``Group`` model with details, and
        the list view has less fields than the detail.
        """

        class Meta:
            model = Group
            fields = ('id', 'name', 'permissions')
            action_fields = {
                'list': {
                    'fields': ('id', 'name'),
                },
            }

In your ViewSet, just set the serializer like normal:

.. code-block:: python

    from rest_framework.viewsets import ModelViewSet


    class GroupViewSet(ModelViewSet):
        """
        An example viewset for the Django ``Group`` model.
        """
        serializer_class = GroupActionSerializer
        queryset = Group.objects.all()


Tests
=====

.. code-block:: shell

    $ python manage.py test
