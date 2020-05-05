import pytest
from rest_framework import status

from ...dados_comuns import constants
from ...dados_comuns.fluxo_status import HomologacaoProdutoWorkflow

pytestmark = pytest.mark.django_db


def test_url_endpoint_homologacao_produto_codae_homologa(client_autenticado_vinculo_codae_produto,
                                                         homologacao_produto_pendente_homologacao):
    assert homologacao_produto_pendente_homologacao.status == HomologacaoProdutoWorkflow.CODAE_PENDENTE_HOMOLOGACAO
    response = client_autenticado_vinculo_codae_produto.patch(
        f'/homologacoes-produtos/{homologacao_produto_pendente_homologacao.uuid}/{constants.CODAE_HOMOLOGA}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == HomologacaoProdutoWorkflow.CODAE_HOMOLOGADO
    response = client_autenticado_vinculo_codae_produto.patch(
        f'/homologacoes-produtos/{homologacao_produto_pendente_homologacao.uuid}/{constants.CODAE_HOMOLOGA}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'codae_homologa' isn't available from state "
                  "'CODAE_HOMOLOGADO'."}
    response = client_autenticado_vinculo_codae_produto.get(
        f'/painel-gerencial-homologacoes-produtos/homologados/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get('results')) == 1


def test_url_endpoint_homologacao_produto_codae_nao_homologa(client_autenticado_vinculo_codae_produto,
                                                             homologacao_produto_pendente_homologacao):
    assert homologacao_produto_pendente_homologacao.status == HomologacaoProdutoWorkflow.CODAE_PENDENTE_HOMOLOGACAO
    response = client_autenticado_vinculo_codae_produto.patch(
        f'/homologacoes-produtos/{homologacao_produto_pendente_homologacao.uuid}/{constants.CODAE_NAO_HOMOLOGA}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == HomologacaoProdutoWorkflow.CODAE_NAO_HOMOLOGADO
    response = client_autenticado_vinculo_codae_produto.patch(
        f'/homologacoes-produtos/{homologacao_produto_pendente_homologacao.uuid}/{constants.CODAE_NAO_HOMOLOGA}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'codae_nao_homologa' isn't available from state "
                  "'CODAE_NAO_HOMOLOGADO'."}
    response = client_autenticado_vinculo_codae_produto.get(
        f'/painel-gerencial-homologacoes-produtos/nao-homologados/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get('results')) == 1


def test_url_endpoint_homologacao_produto_codae_questiona(client_autenticado_vinculo_codae_produto,
                                                          homologacao_produto_pendente_homologacao):
    assert homologacao_produto_pendente_homologacao.status == HomologacaoProdutoWorkflow.CODAE_PENDENTE_HOMOLOGACAO
    response = client_autenticado_vinculo_codae_produto.patch(
        f'/homologacoes-produtos/{homologacao_produto_pendente_homologacao.uuid}/'
        f'{constants.CODAE_QUESTIONA_PEDIDO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == HomologacaoProdutoWorkflow.CODAE_QUESTIONADO
    response = client_autenticado_vinculo_codae_produto.patch(
        f'/homologacoes-produtos/{homologacao_produto_pendente_homologacao.uuid}/'
        f'{constants.CODAE_QUESTIONA_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'codae_questiona' isn't available from state "
                  "'CODAE_QUESTIONADO'."}
    response = client_autenticado_vinculo_codae_produto.get(
        f'/painel-gerencial-homologacoes-produtos/correcao-de-produto/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get('results')) == 1


def test_url_endpoint_homologacao_produto_codae_pede_analise_sensorial(client_autenticado_vinculo_codae_produto,
                                                                       homologacao_produto_pendente_homologacao):
    assert homologacao_produto_pendente_homologacao.status == HomologacaoProdutoWorkflow.CODAE_PENDENTE_HOMOLOGACAO
    response = client_autenticado_vinculo_codae_produto.patch(
        f'/homologacoes-produtos/{homologacao_produto_pendente_homologacao.uuid}/'
        f'{constants.CODAE_PEDE_ANALISE_SENSORIAL}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == HomologacaoProdutoWorkflow.CODAE_PEDIU_ANALISE_SENSORIAL
    response = client_autenticado_vinculo_codae_produto.patch(
        f'/homologacoes-produtos/{homologacao_produto_pendente_homologacao.uuid}/'
        f'{constants.CODAE_PEDE_ANALISE_SENSORIAL}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'codae_pede_analise_sensorial' isn't available from state "
                  "'CODAE_PEDIU_ANALISE_SENSORIAL'."}
    response = client_autenticado_vinculo_codae_produto.get(
        f'/painel-gerencial-homologacoes-produtos/aguardando-analise-sensorial/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get('results')) == 1
