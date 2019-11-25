from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from sme_terceirizadas.paineis_consolidados.api.constants import FILTRO_DATA_INICIAL, TIPO_SOLICITACAO, \
    STATUS_SOLICITACAO, DATA_INICIAL, DATA_FINAL
from ...dados_comuns.constants import FILTRO_PADRAO_PEDIDOS, SEM_FILTRO
from ...paineis_consolidados.api.constants import PESQUISA, TIPO_VISAO, TIPO_VISAO_LOTE, TIPO_VISAO_SOLICITACOES
from ...paineis_consolidados.api.serializers import SolicitacoesSerializer
from ..api.constants import FILTRO_PERIOD_UUID_DRE, PENDENTES_VALIDACAO_DRE
from ..models import (
    FiltrosConsolidados,
    SolicitacoesCODAE,
    SolicitacoesDRE,
    SolicitacoesEscola,
    SolicitacoesTerceirizada
)
from .constants import (
    AUTORIZADOS,
    CANCELADOS,
    FILTRO_DRE_UUID,
    FILTRO_ESCOLA_UUID,
    FILTRO_TERCEIRIZADA_UUID,
    NEGADOS,
    PENDENTES_AUTORIZACAO,
    PENDENTES_CIENCIA
)


class SolicitacoesViewSet(viewsets.ReadOnlyModelViewSet):

    def _agrupar_solicitacoes(self, tipo_visao: str, query_set: QuerySet):
        if tipo_visao == TIPO_VISAO_SOLICITACOES:
            descricao_prioridade = [(solicitacao.desc_doc, solicitacao.prioridade) for solicitacao in query_set
                                    if solicitacao.prioridade != 'VENCIDO']
        elif tipo_visao == TIPO_VISAO_LOTE:
            descricao_prioridade = [(solicitacao.lote_nome, solicitacao.prioridade) for solicitacao in query_set
                                    if solicitacao.prioridade != 'VENCIDO']
        else:
            descricao_prioridade = [(solicitacao.dre_nome, solicitacao.prioridade) for solicitacao in query_set
                                    if solicitacao.prioridade != 'VENCIDO']
        return descricao_prioridade

    def _agrupa_por_tipo_visao(self, tipo_visao: str, query_set: QuerySet) -> dict:
        sumario = {}  # type: dict
        descricao_prioridade = self._agrupar_solicitacoes(tipo_visao, query_set)
        for nome_objeto, prioridade in descricao_prioridade:
            if nome_objeto == 'Inclusão de Alimentação Contínua':
                nome_objeto = 'Inclusão de Alimentação'
            if nome_objeto not in sumario:
                sumario[nome_objeto] = {'TOTAL': 0,
                                        'REGULAR': 0,
                                        'PRIORITARIO': 0,
                                        'LIMITE': 0}
            sumario[nome_objeto][prioridade] += 1
            sumario[nome_objeto]['TOTAL'] += 1
        return sumario

    def _agrupa_por_mes_por_solicitacao(self, query_set: list) -> dict:
        # TODO: melhorar performance
        sumario = {'total': 0}  # type: dict
        for solicitacao in query_set:
            if solicitacao['desc_doc'] == 'Inclusão de Alimentação Contínua':
                solicitacao['desc_doc'] = 'Inclusão de Alimentação'
            if solicitacao['desc_doc'] not in sumario:
                sumario[solicitacao['desc_doc']] = {
                    'quantidades': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    'total': 0
                }
            sumario[solicitacao['desc_doc']]['quantidades'][solicitacao['data_evento__month'] - 1] += 1
            sumario[solicitacao['desc_doc']]['total'] += 1
            sumario['total'] += 1
        return sumario


class CODAESolicitacoesViewSet(SolicitacoesViewSet):
    lookup_field = 'uuid'
    queryset = SolicitacoesCODAE.objects.all()
    serializer_class = SolicitacoesSerializer

    @action(detail=False, methods=['GET'], url_path=f'{PENDENTES_AUTORIZACAO}/{FILTRO_PADRAO_PEDIDOS}')
    def pendentes_autorizacao(self, request, filtro_aplicado=SEM_FILTRO):
        query_set = SolicitacoesCODAE.get_pendentes_autorizacao(filtro=filtro_aplicado)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=AUTORIZADOS)
    def autorizados(self, request):
        query_set = SolicitacoesCODAE.get_autorizados()
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=NEGADOS)
    def negados(self, request):
        query_set = SolicitacoesCODAE.get_negados()
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=CANCELADOS)
    def cancelados(self, request):
        query_set = SolicitacoesCODAE.get_cancelados()
        return self._retorno_base(query_set)

    def _retorno_base(self, query_set):
        page = self.paginate_queryset(query_set)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class EscolaSolicitacoesViewSet(SolicitacoesViewSet):
    lookup_field = 'uuid'
    queryset = SolicitacoesEscola.objects.all()
    serializer_class = SolicitacoesSerializer

    @action(detail=False, methods=['GET'], url_path=f'{PENDENTES_AUTORIZACAO}/{FILTRO_ESCOLA_UUID}')
    def pendentes_autorizacao(self, request, escola_uuid=None):
        query_set = SolicitacoesEscola.get_pendentes_autorizacao(escola_uuid=escola_uuid)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=f'{AUTORIZADOS}/{FILTRO_ESCOLA_UUID}')
    def autorizados(self, request, escola_uuid=None):
        query_set = SolicitacoesEscola.get_autorizados(escola_uuid=escola_uuid)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=f'{NEGADOS}/{FILTRO_ESCOLA_UUID}')
    def negados(self, request, escola_uuid=None):
        query_set = SolicitacoesEscola.get_negados(escola_uuid=escola_uuid)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=f'{CANCELADOS}/{FILTRO_ESCOLA_UUID}')
    def cancelados(self, request, escola_uuid=None):
        query_set = SolicitacoesEscola.get_cancelados(escola_uuid=escola_uuid)
        return self._retorno_base(query_set)

    # TODO: achar uma forma melhor de estruturar isso. Ex: pesquisa/uuidEscola?tipo=XXX&status=zzz&data_inicial=DDDD
    @action(
        detail=False,
        methods=['GET'],
        url_path=f'{PESQUISA}/{FILTRO_ESCOLA_UUID}/{TIPO_SOLICITACAO}/{STATUS_SOLICITACAO}/{DATA_INICIAL}/{DATA_FINAL}')
    def filtro_periodo_tipo_solicitacao(self, request, escola_uuid=None, data_inicial=None, data_final=None,
                                        tipo_solicitacao='TODOS', status_solicitacao='TODOS'):
        query_set = FiltrosConsolidados.filtros_escola(
            escola_uuid=escola_uuid,
            data_inicial=data_inicial,
            data_final=data_final,
            tipo_solicitacao=tipo_solicitacao,
            status_solicitacao=status_solicitacao
        )

        return self._retorno_base(query_set)

    def _retorno_base(self, query_set):
        page = self.paginate_queryset(query_set)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class EscolaRelatorioViewSet(SolicitacoesViewSet):
    queryset = SolicitacoesEscola.objects.all()
    serializer_class = SolicitacoesSerializer

    @action(detail=False, methods=['GET'])
    def evolucao_solicitacoes(self, request):
        usuario = request.user
        escola_uuid = usuario.vinculo_atual.instituicao.uuid
        query_set = SolicitacoesEscola.get_solicitacoes_ano_corrente(escola_uuid=escola_uuid)
        response = {'results': self._agrupa_por_mes_por_solicitacao(query_set=query_set)}
        return Response(response)


class DRESolicitacoesViewSet(SolicitacoesViewSet):
    lookup_field = 'uuid'
    queryset = SolicitacoesDRE.objects.all()
    serializer_class = SolicitacoesSerializer

    @action(detail=False, methods=['GET'], url_path=f'{PENDENTES_AUTORIZACAO}/{FILTRO_DRE_UUID}')
    def pendentes_autorizacao(self, request, dre_uuid=None):
        query_set = SolicitacoesDRE.get_pendentes_autorizacao(dre_uuid=dre_uuid)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=f'{PENDENTES_VALIDACAO_DRE}/{FILTRO_PERIOD_UUID_DRE}')
    def pendentes_validacao(self, request, dre_uuid=None, filtro_aplicado=SEM_FILTRO):
        query_set = SolicitacoesDRE.get_pendentes_validacao(dre_uuid=dre_uuid, filtro_aplicado=filtro_aplicado)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=f'{AUTORIZADOS}/{FILTRO_DRE_UUID}')
    def autorizados(self, request, dre_uuid=None):
        query_set = SolicitacoesDRE.get_autorizados(dre_uuid=dre_uuid)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=f'{NEGADOS}/{FILTRO_DRE_UUID}')
    def negados(self, request, dre_uuid=None):
        query_set = SolicitacoesDRE.get_negados(dre_uuid=dre_uuid)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=f'{CANCELADOS}/{FILTRO_DRE_UUID}')
    def cancelados(self, request, dre_uuid=None):
        query_set = SolicitacoesDRE.get_cancelados(dre_uuid=dre_uuid)
        return self._retorno_base(query_set)

    def _retorno_base(self, query_set):
        page = self.paginate_queryset(query_set)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class TerceirizadaSolicitacoesViewSet(SolicitacoesViewSet):
    lookup_field = 'uuid'
    queryset = SolicitacoesTerceirizada.objects.all()
    serializer_class = SolicitacoesSerializer

    @action(detail=False, methods=['GET'], url_path=f'{PENDENTES_AUTORIZACAO}/{FILTRO_TERCEIRIZADA_UUID}')
    def pendentes_autorizacao(self, request, terceirizada_uuid=None):
        query_set = SolicitacoesTerceirizada.get_pendentes_autorizacao(terceirizada_uuid=terceirizada_uuid)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=f'{AUTORIZADOS}/{FILTRO_TERCEIRIZADA_UUID}')
    def autorizados(self, request, terceirizada_uuid=None):
        query_set = SolicitacoesTerceirizada.get_autorizados(terceirizada_uuid=terceirizada_uuid)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=f'{NEGADOS}/{FILTRO_TERCEIRIZADA_UUID}')
    def negados(self, request, terceirizada_uuid=None):
        query_set = SolicitacoesTerceirizada.get_negados(terceirizada_uuid=terceirizada_uuid)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'], url_path=f'{CANCELADOS}/{FILTRO_TERCEIRIZADA_UUID}')
    def cancelados(self, request, terceirizada_uuid=None):
        query_set = SolicitacoesTerceirizada.get_cancelados(terceirizada_uuid=terceirizada_uuid)
        return self._retorno_base(query_set)

    @action(detail=False, methods=['GET'],
            url_path=f'{PENDENTES_CIENCIA}/{FILTRO_TERCEIRIZADA_UUID}/{FILTRO_PADRAO_PEDIDOS}/{TIPO_VISAO}')
    def pendentes_ciencia(self, request, terceirizada_uuid=None, filtro_aplicado=SEM_FILTRO,
                          tipo_visao=TIPO_VISAO_SOLICITACOES):
        query_set = SolicitacoesTerceirizada.get_pendentes_ciencia(terceirizada_uuid=terceirizada_uuid,
                                                                   filtro=filtro_aplicado)
        response = {'results': self._agrupa_por_tipo_visao(tipo_visao=tipo_visao, query_set=query_set)}
        return Response(response)

    def _retorno_base(self, query_set):
        page = self.paginate_queryset(query_set)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
