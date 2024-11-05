from rest_framework.exceptions import MethodNotAllowed


class UpdateMixin:
    """Миксин для запрета метода PUT."""

    def perform_update(self, serializer):
        if self.request.method == 'PUT':
            raise MethodNotAllowed('Метод PUT запрещен')
        super().perform_update(serializer)
