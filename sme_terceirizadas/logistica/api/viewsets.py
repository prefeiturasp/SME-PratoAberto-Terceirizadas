from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from xworkflows import InvalidTransitionError

from sme_terceirizadas.dados_comuns.parser_xml import ListXMLParser
from sme_terceirizadas.dados_comuns.models import LogSolicitacoesUsuario
from sme_terceirizadas.logistica.api.serializers.serializer_create import SolicitacaoRemessaCreateSerializer
from sme_terceirizadas.logistica.api.serializers.serializers import (
    SolicitacaoRemessaSerializer,
    XmlParserSolicitacaoSerializer
)
from sme_terceirizadas.logistica.models import SolicitacaoRemessa

from sme_terceirizadas.perfil.models import Usuario

STR_XML_BODY = '{http://schemas.xmlsoap.org/soap/envelope/}Body'
STR_ARQUIVO_SOLICITACAO = 'ArqSolicitacaoMOD'


class SolicitacaoModelViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    http_method_names = ['get', 'post', 'patch']
    queryset = SolicitacaoRemessa.objects.all()
    serializer_class = SolicitacaoRemessaCreateSerializer
    permission_classes = [AllowAny]
    parser_classes = (ListXMLParser,)

    def get_serializer_class(self):
        if self.action == 'create':
            return XmlParserSolicitacaoSerializer
        return SolicitacaoRemessaSerializer

    def create(self, request, *args, **kwargs):
        remove_dirt = request.data.get(f'{STR_XML_BODY}')
        json_data = remove_dirt.pop(f'{STR_ARQUIVO_SOLICITACAO}')
        instance = SolicitacaoRemessaCreateSerializer().create(validated_data=json_data)
        # TODO: criar perfil e usuario PAPA e pegar usuario da request e imputar no log
        usuario = Usuario.objects.get(email='dilog@admin.com')

        instance.salvar_log_transicao(
            status_evento=LogSolicitacoesUsuario.INICIO_FLUXO_SOLICITACAO,
            usuario=usuario
        )
        serializer = SolicitacaoRemessaSerializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, permission_classes=(AllowAny,),
            methods=['patch'], url_path='envia-solicitacao')
    def incia_fluxo_solicitacao(self, request, uuid=None):
        solicitacao = SolicitacaoRemessa.objects.get(uuid=uuid)
        # TODO: criar permission class para DILOG e pegar usuario da requisicao e sibistituir a linha abaixo
        usuario = Usuario.objects.get(email='dilog@admin.com')

        try:
            solicitacao.inicia_fluxo(user=usuario, )
            serializer = SolicitacaoRemessaSerializer(solicitacao)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=(AllowAny,),
            methods=['patch'], url_path='distribuidor-confirma')
    def distribuidor_confirma_hook(self, request, uuid=None):
        solicitacao = SolicitacaoRemessa.objects.get(uuid=uuid)
        # TODO: criar permission class e pegar usuario da requisicao e sibistituir a linha abaixo
        usuario = Usuario.objects.get(email='dilog@admin.com')
        
        try:
            solicitacao.empresa_atende(user=usuario, )
            serializer = SolicitacaoRemessaSerializer(solicitacao)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=status.HTTP_400_BAD_REQUEST)
