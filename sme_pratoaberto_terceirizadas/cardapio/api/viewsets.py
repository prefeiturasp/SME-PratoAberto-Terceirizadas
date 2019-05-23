from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from sme_pratoaberto_terceirizadas.users.models import User
from sme_pratoaberto_terceirizadas.utils import send_notification, send_email
from .serializers import AlteracaoCardapioSerializer
from ..models import AlteracaoCardapio

cintia_qs = User.objects.filter(email='cintia.ramos@amcom.com.br')


class AlteracaoCardapioViewSet(ModelViewSet):
    queryset = AlteracaoCardapio.objects.all()
    serializer_class = AlteracaoCardapioSerializer
    lookup_field = 'uuid'

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().create(request, *args, **kwargs)
        if response:
            # TODO: implementar logica das partes interessadas na notificação...
            short_desc = 'Alteração de cardápio criada'.format(response.data.get('id', None))
            send_notification(sender=request.user, recipients=cintia_qs,
                              short_desc=short_desc, long_desc=response.data)
            send_email(short_desc, str(response.data), 'mmaia.cc@gmail.com')
        return response

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().partial_update(request, *args, **kwargs)
        if response:
            alt_id = response.data.get('id', None)
            status = response.data.get('status', None)
            short_desc = 'Alteração de cardápio #{} atualizada para: {}'.format(
                alt_id, status)
            send_notification(sender=request.user, recipients=cintia_qs,
                              short_desc=short_desc, long_desc=response.data)

            send_email(short_desc, str(response.data), 'mmaia.cc@gmail.com')
        return response
