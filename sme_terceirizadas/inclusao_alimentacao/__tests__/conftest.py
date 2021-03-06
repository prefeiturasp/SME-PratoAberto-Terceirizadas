import datetime

import pytest
from faker import Faker
from model_mommy import mommy

from ...dados_comuns import constants
from ...dados_comuns.fluxo_status import PedidoAPartirDaEscolaWorkflow
from ...dados_comuns.models import TemplateMensagem
from .. import models

fake = Faker('pt-Br')
fake.seed(420)


@pytest.fixture
def codae():
    return mommy.make('Codae')


@pytest.fixture
def escola():
    terceirizada = mommy.make('Terceirizada')
    lote = mommy.make('Lote', terceirizada=terceirizada)
    diretoria_regional = mommy.make('DiretoriaRegional', nome='DIRETORIA REGIONAL IPIRANGA',
                                    uuid='9640fef4-a068-474e-8979-2e1b2654357a')
    return mommy.make('Escola', lote=lote, diretoria_regional=diretoria_regional)


@pytest.fixture
def dre_guaianases():
    return mommy.make('DiretoriaRegional', nome='DIRETORIA REGIONAL GUAIANASES')


@pytest.fixture
def escola_dre_guaianases(dre_guaianases):
    lote = mommy.make('Lote')
    return mommy.make('Escola', lote=lote, diretoria_regional=dre_guaianases)


@pytest.fixture
def motivo_inclusao_continua():
    return mommy.make(models.MotivoInclusaoContinua, nome='teste nome')


@pytest.fixture
def motivo_inclusao_normal():
    return mommy.make(models.MotivoInclusaoNormal, nome=fake.name())


@pytest.fixture
def quantidade_por_periodo():
    periodo_escolar = mommy.make('escola.PeriodoEscolar')
    tipos_alimentacao = mommy.make('cardapio.ComboDoVinculoTipoAlimentacaoPeriodoTipoUE', _quantity=5, make_m2m=True)

    return mommy.make(models.QuantidadePorPeriodo,
                      numero_alunos=0,
                      periodo_escolar=periodo_escolar,
                      tipos_alimentacao=tipos_alimentacao)


@pytest.fixture
def template_inclusao_normal():
    return mommy.make(TemplateMensagem, assunto='TESTE',
                      tipo=TemplateMensagem.INCLUSAO_ALIMENTACAO,
                      template_html='@id @criado_em @status @link')


@pytest.fixture
def template_inclusao_continua():
    return mommy.make(TemplateMensagem, assunto='TESTE',
                      tipo=TemplateMensagem.INCLUSAO_ALIMENTACAO_CONTINUA,
                      template_html='@id @criado_em @status @link')


@pytest.fixture(params=[
    # data ini, data fim, esperado
    (datetime.date(2019, 10, 1), datetime.date(2019, 10, 30), datetime.date(2019, 10, 1)),
    (datetime.date(2019, 10, 1), datetime.date(2019, 9, 20), datetime.date(2019, 9, 20))
]
)
def inclusao_alimentacao_continua_params(escola, motivo_inclusao_continua, request, template_inclusao_continua):
    data_inicial, data_final, esperado = request.param
    model = mommy.make(models.InclusaoAlimentacaoContinua,
                       uuid='98dc7cb7-7a38-408d-907c-c0f073ca2d13',
                       motivo=motivo_inclusao_continua,
                       data_inicial=data_inicial,
                       data_final=data_final,
                       outro_motivo=fake.name(),
                       escola=escola)
    return model, esperado


@pytest.fixture(params=[
    # data ini, data fim, esperado
    (datetime.date(2019, 10, 1), datetime.date(2019, 10, 30), datetime.date(2019, 10, 1)),
    (datetime.date(2019, 10, 1), datetime.date(2019, 9, 20), datetime.date(2019, 9, 20))]
)
def inclusao_alimentacao_continua(escola, motivo_inclusao_continua, request, template_inclusao_continua):
    data_inicial, data_final, esperado = request.param
    return mommy.make(models.InclusaoAlimentacaoContinua,
                      motivo=motivo_inclusao_continua,
                      data_inicial=data_inicial,
                      data_final=data_final,
                      outro_motivo=fake.name(),
                      escola=escola,
                      rastro_escola=escola,
                      rastro_dre=escola.diretoria_regional)


@pytest.fixture(params=[
    # data ini, data fim, esperado
    (datetime.date(2019, 10, 1), datetime.date(2019, 10, 30), datetime.date(2019, 10, 1)),
    (datetime.date(2019, 10, 1), datetime.date(2019, 9, 20), datetime.date(2019, 9, 20))]
)
def inclusao_alimentacao_continua_outra_dre(escola_dre_guaianases, motivo_inclusao_continua, request,
                                            template_inclusao_continua):
    data_inicial, data_final, esperado = request.param
    return mommy.make(models.InclusaoAlimentacaoContinua,
                      motivo=motivo_inclusao_continua,
                      data_inicial=data_inicial,
                      data_final=data_final,
                      outro_motivo=fake.name(),
                      escola=escola_dre_guaianases,
                      rastro_escola=escola_dre_guaianases,
                      rastro_dre=escola_dre_guaianases.diretoria_regional)


@pytest.fixture
def inclusao_alimentacao_continua_dre_validar(inclusao_alimentacao_continua):
    inclusao_alimentacao_continua.status = PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    inclusao_alimentacao_continua.save()
    return inclusao_alimentacao_continua


@pytest.fixture
def inclusao_alimentacao_continua_dre_validado(inclusao_alimentacao_continua):
    inclusao_alimentacao_continua.status = PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    inclusao_alimentacao_continua.save()
    return inclusao_alimentacao_continua


@pytest.fixture
def inclusao_alimentacao_continua_codae_autorizado(inclusao_alimentacao_continua):
    inclusao_alimentacao_continua.status = PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    inclusao_alimentacao_continua.save()
    return inclusao_alimentacao_continua


@pytest.fixture
def inclusao_alimentacao_continua_codae_questionado(inclusao_alimentacao_continua):
    inclusao_alimentacao_continua.status = PedidoAPartirDaEscolaWorkflow.CODAE_QUESTIONADO
    inclusao_alimentacao_continua.save()
    return inclusao_alimentacao_continua


@pytest.fixture
def inclusao_alimentacao_normal(motivo_inclusao_normal):
    return mommy.make(models.InclusaoAlimentacaoNormal,
                      data=datetime.date(2019, 10, 1),
                      motivo=motivo_inclusao_normal)


@pytest.fixture
def inclusao_alimentacao_normal_outro_motivo(motivo_inclusao_normal):
    return mommy.make(models.InclusaoAlimentacaoNormal,
                      data=datetime.date(2019, 10, 1),
                      motivo=motivo_inclusao_normal,
                      outro_motivo=fake.name())


@pytest.fixture(params=[
    # data ini, data fim, esperado
    (datetime.date(2019, 10, 1), datetime.date(2019, 10, 30)),
    (datetime.date(2019, 10, 1), datetime.date(2019, 9, 20))]
)
def grupo_inclusao_alimentacao_normal(escola, motivo_inclusao_normal, request, template_inclusao_normal):
    data_1, data_2 = request.param
    grupo_inclusao_normal = mommy.make(models.GrupoInclusaoAlimentacaoNormal,
                                       escola=escola,
                                       rastro_escola=escola,
                                       rastro_dre=escola.diretoria_regional)
    mommy.make(models.InclusaoAlimentacaoNormal,
               data=data_1,
               motivo=motivo_inclusao_normal,
               grupo_inclusao=grupo_inclusao_normal)
    mommy.make(models.InclusaoAlimentacaoNormal,
               data=data_2,
               motivo=motivo_inclusao_normal,
               grupo_inclusao=grupo_inclusao_normal)
    return grupo_inclusao_normal


@pytest.fixture(params=[
    # data ini, data fim, esperado
    (datetime.date(2019, 10, 1), datetime.date(2019, 10, 30)),
    (datetime.date(2019, 10, 1), datetime.date(2019, 9, 20))]
)
def grupo_inclusao_alimentacao_normal_outra_dre(escola_dre_guaianases,
                                                motivo_inclusao_normal,
                                                request,
                                                template_inclusao_normal):
    data_1, data_2 = request.param
    grupo_inclusao_normal = mommy.make(models.GrupoInclusaoAlimentacaoNormal,
                                       escola=escola_dre_guaianases,
                                       rastro_escola=escola_dre_guaianases,
                                       rastro_dre=escola_dre_guaianases.diretoria_regional)
    mommy.make(models.InclusaoAlimentacaoNormal,
               data=data_1,
               motivo=motivo_inclusao_normal,
               grupo_inclusao=grupo_inclusao_normal)
    mommy.make(models.InclusaoAlimentacaoNormal,
               data=data_2,
               motivo=motivo_inclusao_normal,
               grupo_inclusao=grupo_inclusao_normal)
    return grupo_inclusao_normal


@pytest.fixture
def grupo_inclusao_alimentacao_normal_dre_validar(grupo_inclusao_alimentacao_normal):
    grupo_inclusao_alimentacao_normal.status = PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    grupo_inclusao_alimentacao_normal.save()
    return grupo_inclusao_alimentacao_normal


@pytest.fixture
def grupo_inclusao_alimentacao_normal_dre_validado(grupo_inclusao_alimentacao_normal):
    grupo_inclusao_alimentacao_normal.status = PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    grupo_inclusao_alimentacao_normal.save()
    return grupo_inclusao_alimentacao_normal


@pytest.fixture
def grupo_inclusao_alimentacao_normal_codae_autorizado(grupo_inclusao_alimentacao_normal):
    grupo_inclusao_alimentacao_normal.status = PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    grupo_inclusao_alimentacao_normal.save()
    return grupo_inclusao_alimentacao_normal


@pytest.fixture
def grupo_inclusao_alimentacao_normal_codae_questionado(grupo_inclusao_alimentacao_normal):
    grupo_inclusao_alimentacao_normal.status = PedidoAPartirDaEscolaWorkflow.CODAE_QUESTIONADO
    grupo_inclusao_alimentacao_normal.save()
    return grupo_inclusao_alimentacao_normal


@pytest.fixture(params=[
    # data_inicial, data_final
    (datetime.date(2019, 10, 4), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 5), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 6), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 7), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 8), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 9), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 10), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 11), datetime.date(2019, 12, 31)),
])
def inclusao_alimentacao_continua_parametros_semana(request):
    return request.param


@pytest.fixture(params=[
    # data_inicial, data_final
    (datetime.date(2019, 10, 4), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 5), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 10), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 20), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 25), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 31), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 11, 3), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 11, 4), datetime.date(2019, 12, 31)),
])
def inclusao_alimentacao_continua_parametros_mes(request):
    return request.param


@pytest.fixture(params=[
    # data_inicial, data_final, status
    (datetime.date(2019, 10, 3), datetime.date(2019, 12, 31), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    (datetime.date(2019, 10, 2), datetime.date(2019, 12, 31), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    (datetime.date(2019, 10, 1), datetime.date(2019, 12, 31), PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO),
    (datetime.date(2019, 10, 1), datetime.date(2019, 12, 31), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
])
def inclusao_alimentacao_continua_parametros_vencidos(request):
    return request.param


@pytest.fixture(params=[
    # data_inicial, data_final, dias semana,
    (datetime.date(2019, 10, 20), datetime.date(2019, 10, 30), [1, 2, 3, 4, 5, 6]),
    (datetime.date(2020, 10, 17), datetime.date(2020, 10, 30), [1, 2, 3]),
    (datetime.date(2020, 3, 1), datetime.date(2020, 3, 31), [1, 2, 3, 4]),
    (datetime.date(2020, 8, 17), datetime.date(2020, 9, 30), [1, 4])
])
def inclusao_alimentacao_continua_parametros(request):
    return request.param


@pytest.fixture
def motivo_inclusao_normal_nome():
    return mommy.make(models.MotivoInclusaoNormal, nome='Passeio 5h')


@pytest.fixture
def grupo_inclusao_alimentacao_nome():
    return mommy.make(models.GrupoInclusaoAlimentacaoNormal)


@pytest.fixture
def client_autenticado_vinculo_escola_inclusao(client, django_user_model, escola, template_inclusao_normal):
    email = 'test@test.com'
    password = 'bar'
    user = django_user_model.objects.create_user(password=password, email=email,
                                                 registro_funcional='8888888')
    perfil_diretor = mommy.make('Perfil', nome=constants.DIRETOR, ativo=True)
    hoje = datetime.date.today()
    mommy.make('Vinculo', usuario=user, instituicao=escola, perfil=perfil_diretor,
               data_inicial=hoje, ativo=True)
    client.login(email=email, password=password)
    return client


@pytest.fixture
def client_autenticado_vinculo_escola_cei_inclusao(client, django_user_model, escola, template_inclusao_normal):
    email = 'test@test.com'
    password = 'bar'
    user = django_user_model.objects.create_user(password=password, email=email,
                                                 registro_funcional='8888888')
    perfil_diretor = mommy.make('Perfil', nome=constants.DIRETOR_CEI, ativo=True)
    hoje = datetime.date.today()
    mommy.make('Vinculo', usuario=user, instituicao=escola, perfil=perfil_diretor,
               data_inicial=hoje, ativo=True)
    client.login(email=email, password=password)
    return client


@pytest.fixture
def client_autenticado_vinculo_dre_inclusao(client, django_user_model, escola, template_inclusao_normal):
    email = 'test@test1.com'
    password = 'bar'
    user = django_user_model.objects.create_user(password=password, email=email,
                                                 registro_funcional='8888889')
    perfil_cogestor = mommy.make('Perfil', nome='COGESTOR', ativo=True)
    hoje = datetime.date.today()
    mommy.make('Vinculo', usuario=user, instituicao=escola.diretoria_regional, perfil=perfil_cogestor,
               data_inicial=hoje, ativo=True)
    client.login(email=email, password=password)
    return client


@pytest.fixture
def client_autenticado_vinculo_codae_inclusao(client, django_user_model, escola, codae):
    email = 'test@test.com'
    password = 'bar'
    user = django_user_model.objects.create_user(password=password, email=email,
                                                 registro_funcional='8888888')
    perfil_admin_gestao_alimentacao = mommy.make('Perfil', nome=constants.ADMINISTRADOR_GESTAO_ALIMENTACAO_TERCEIRIZADA,
                                                 ativo=True,
                                                 uuid='41c20c8b-7e57-41ed-9433-ccb92e8afaf1')
    hoje = datetime.date.today()
    mommy.make('Vinculo', usuario=user, instituicao=codae, perfil=perfil_admin_gestao_alimentacao,
               data_inicial=hoje, ativo=True)
    mommy.make(TemplateMensagem, assunto='TESTE',
               tipo=TemplateMensagem.DIETA_ESPECIAL,
               template_html='@id @criado_em @status @link')
    client.login(email=email, password=password)
    return client


@pytest.fixture
def client_autenticado_vinculo_terceirizada_inclusao(client, django_user_model, escola, codae):
    email = 'test@test.com'
    password = 'bar'
    user = django_user_model.objects.create_user(password=password, email=email,
                                                 registro_funcional='8888888')
    perfil_nutri_admin = mommy.make('Perfil', nome=constants.NUTRI_ADMIN_RESPONSAVEL,
                                    ativo=True,
                                    uuid='41c20c8b-7e57-41ed-9433-ccb92e8afaf1')
    hoje = datetime.date.today()
    mommy.make('Vinculo', usuario=user, instituicao=escola.lote.terceirizada, perfil=perfil_nutri_admin,
               data_inicial=hoje, ativo=True)
    mommy.make(TemplateMensagem, assunto='TESTE',
               tipo=TemplateMensagem.DIETA_ESPECIAL,
               template_html='@id @criado_em @status @link')
    client.login(email=email, password=password)
    return client
