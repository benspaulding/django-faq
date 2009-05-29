from django.dispatch import Signal


published = Signal(providing_args=('instance', 'created'))
unpublished = Signal(providing_args=('instance', 'deleted'))
sites_changed = Signal(providing_args=('instance', ))
