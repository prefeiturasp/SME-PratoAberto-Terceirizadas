from django.core.validators import MinLengthValidator
from django.db import models

from ..cardapio.models import (
    AlteracaoCardapio,
    InversaoCardapio
)
from ..dados_comuns.models_abstract import (
    Ativavel, IntervaloDeDia, Nomeavel, TemChaveExterna, TemIdentificadorExternoAmigavel
)
from ..escola.models import (
    DiretoriaRegional, Lote
)
from ..inclusao_alimentacao.models import (
    GrupoInclusaoAlimentacaoNormal, InclusaoAlimentacaoContinua
)
from ..kit_lanche.models import (
    SolicitacaoKitLancheAvulsa,
    SolicitacaoKitLancheUnificada
)


class Edital(TemChaveExterna):
    numero = models.CharField('Edital No', max_length=100, help_text='Número do Edital', unique=True)
    tipo_contratacao = models.CharField('Tipo de contratação', max_length=100)
    processo = models.CharField('Processo Administrativo', max_length=100,
                                help_text='Processo administrativo do edital')
    objeto = models.TextField('objeto resumido')

    @property
    def contratos(self):
        return self.contratos

    def __str__(self):
        return f'{self.numero} - {self.objeto}'

    class Meta:
        verbose_name = 'Edital'
        verbose_name_plural = 'Editais'


class Nutricionista(TemChaveExterna, Nomeavel):
    # TODO: verificar a diferença dessa pra nutricionista da CODAE

    crn_numero = models.CharField('Nutricionista crn', max_length=160,
                                  blank=True)
    terceirizada = models.ForeignKey('Terceirizada',
                                     on_delete=models.CASCADE,
                                     related_name='nutricionistas',
                                     blank=True,
                                     null=True)

    # TODO: retornar aqui quando tiver um perfil definido
    contatos = models.ManyToManyField('dados_comuns.Contato', blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Nutricionista'
        verbose_name_plural = 'Nutricionistas'


class Terceirizada(TemChaveExterna, Ativavel, TemIdentificadorExternoAmigavel):

    usuarios = models.ManyToManyField('perfil.Usuario', related_name='terceirizadas', blank=True)
    nome_fantasia = models.CharField('Nome fantasia', max_length=160, blank=True)
    razao_social = models.CharField('Razao social', max_length=160, blank=True)
    cnpj = models.CharField('CNPJ', validators=[MinLengthValidator(14)], max_length=14)
    representante_legal = models.CharField('Representante legal', max_length=160, blank=True)
    representante_telefone = models.CharField('Representante contato (telefone)', max_length=160, blank=True)
    representante_email = models.CharField('Representante contato (email)', max_length=160, blank=True)
    endereco = models.ForeignKey('dados_comuns.Endereco', on_delete=models.CASCADE,
                                 blank=True, null=True)

    # TODO: criar uma tabela central (Instituição) para agregar Escola, DRE, Terc e CODAE???
    # e a partir dai a instituição que tem contatos e endereço?
    # o mesmo para pessoa fisica talvez?
    contatos = models.ManyToManyField('dados_comuns.Contato', blank=True)

    @property
    def nutricionistas(self):
        return self.nutricionistas

    @property
    def inclusoes_continuas_aprovadas(self):
        return InclusaoAlimentacaoContinua.objects.filter(
            escola__lote__in=self.lotes.all(),
            status__in=[InclusaoAlimentacaoContinua.workflow_class.CODAE_AUTORIZADO,
                        InclusaoAlimentacaoContinua.workflow_class.TERCEIRIZADA_TOMA_CIENCIA]
        )

    @property
    def inclusoes_normais_aprovadas(self):
        return GrupoInclusaoAlimentacaoNormal.objects.filter(
            escola__lote__in=self.lotes.all(),
            status__in=[GrupoInclusaoAlimentacaoNormal.workflow_class.CODAE_AUTORIZADO,
                        GrupoInclusaoAlimentacaoNormal.workflow_class.TERCEIRIZADA_TOMA_CIENCIA]
        )

    @property
    def inclusoes_continuas_reprovadas(self):
        return InclusaoAlimentacaoContinua.objects.filter(
            escola__lote__in=self.lotes.all(),
            status=InclusaoAlimentacaoContinua.workflow_class.CODAE_CANCELOU_PEDIDO
        )

    @property
    def solicitacao_kit_lanche_avulsa_aprovadas(self):
        return SolicitacaoKitLancheAvulsa.objects.filter(
            escola__lote__in=self.lotes.all(),
            status__in=[SolicitacaoKitLancheAvulsa.workflow_class.CODAE_AUTORIZADO,
                        SolicitacaoKitLancheAvulsa.workflow_class.TERCEIRIZADA_TOMA_CIENCIA]
        )

    @property
    def inclusoes_normais_reprovadas(self):
        return GrupoInclusaoAlimentacaoNormal.objects.filter(
            escola__lote__in=self.lotes.all(),
            status=GrupoInclusaoAlimentacaoNormal.workflow_class.CODAE_CANCELOU_PEDIDO
        )

    # TODO: talvez fazer um manager genérico pra fazer esse filtro

    def inclusoes_continuas_das_minhas_escolas_no_prazo_vencendo(self, filtro_aplicado):
        if filtro_aplicado == 'hoje':
            inclusoes_continuas = InclusaoAlimentacaoContinua.prazo_vencendo_hoje
        else:  # se o filtro nao for hoje, filtra o padrao
            inclusoes_continuas = InclusaoAlimentacaoContinua.prazo_vencendo
        return inclusoes_continuas.filter(
            status=InclusaoAlimentacaoContinua.workflow_class.CODAE_AUTORIZADO,
            escola__lote__in=self.lotes.all()
        )

    def inclusoes_continuas_das_minhas_escolas_no_prazo_limite(self, filtro_aplicado):
        if filtro_aplicado == 'daqui_a_7_dias':
            inclusoes_continuas = InclusaoAlimentacaoContinua.prazo_limite_daqui_a_7_dias
        else:
            inclusoes_continuas = InclusaoAlimentacaoContinua.prazo_limite
        return inclusoes_continuas.filter(
            status=InclusaoAlimentacaoContinua.workflow_class.CODAE_AUTORIZADO,
            escola__lote__in=self.lotes.all()
        )

    def inclusoes_continuas_das_minhas_escolas_no_prazo_regular(self, filtro_aplicado):
        if filtro_aplicado == 'daqui_a_30_dias':
            inclusoes_continuas = InclusaoAlimentacaoContinua.prazo_regular_daqui_a_30_dias
        elif filtro_aplicado == 'daqui_a_7_dias':
            inclusoes_continuas = InclusaoAlimentacaoContinua.prazo_regular_daqui_a_7_dias
        else:
            inclusoes_continuas = InclusaoAlimentacaoContinua.prazo_regular
        return inclusoes_continuas.filter(
            status=InclusaoAlimentacaoContinua.workflow_class.CODAE_AUTORIZADO,
            escola__lote__in=self.lotes.all()
        )

    def inclusoes_normais_das_minhas_escolas_no_prazo_vencendo(self, filtro_aplicado):
        if filtro_aplicado == 'hoje':
            inclusoes_normais = GrupoInclusaoAlimentacaoNormal.prazo_vencendo_hoje
        else:
            inclusoes_normais = GrupoInclusaoAlimentacaoNormal.prazo_vencendo
        return inclusoes_normais.filter(
            status=InclusaoAlimentacaoContinua.workflow_class.CODAE_AUTORIZADO,
            escola__lote__in=self.lotes.all()
        )

    def inclusoes_normais_das_minhas_escolas_no_prazo_limite(self, filtro_aplicado):
        if filtro_aplicado == 'daqui_a_7_dias':
            inclusoes_normais = GrupoInclusaoAlimentacaoNormal.prazo_limite_daqui_a_7_dias
        else:
            inclusoes_normais = GrupoInclusaoAlimentacaoNormal.prazo_limite
        return inclusoes_normais.filter(
            status=InclusaoAlimentacaoContinua.workflow_class.CODAE_AUTORIZADO,
            escola__lote__in=self.lotes.all()
        )

    def inclusoes_normais_das_minhas_escolas_no_prazo_regular(self, filtro_aplicado):
        if filtro_aplicado == 'daqui_a_30_dias':
            inclusoes_normais = GrupoInclusaoAlimentacaoNormal.prazo_regular_daqui_a_30_dias
        elif filtro_aplicado == 'daqui_a_7_dias':
            inclusoes_normais = GrupoInclusaoAlimentacaoNormal.prazo_regular_daqui_a_7_dias
        else:
            inclusoes_normais = GrupoInclusaoAlimentacaoNormal.prazo_regular
        return inclusoes_normais.filter(
            status=InclusaoAlimentacaoContinua.workflow_class.CODAE_AUTORIZADO,
            escola__lote__in=self.lotes.all()
        )

    def alteracoes_cardapio_das_minhas_escolas_no_prazo_vencendo(self, filtro_aplicado):
        if filtro_aplicado == 'hoje':
            alteracoes_cardapio = AlteracaoCardapio.prazo_vencendo_hoje
        else:
            alteracoes_cardapio = AlteracaoCardapio.prazo_vencendo
        return alteracoes_cardapio.filter(
            status=AlteracaoCardapio.workflow_class.CODAE_AUTORIZADO,
            escola__lote__in=self.lotes.all()
        )

    def alteracoes_cardapio_das_minhas_escolas_no_prazo_limite(self, filtro_aplicado):
        if filtro_aplicado == 'daqui_a_7_dias':
            alteracoes_cardapio = AlteracaoCardapio.prazo_limite_daqui_a_7_dias
        else:
            alteracoes_cardapio = AlteracaoCardapio.prazo_limite
        return alteracoes_cardapio.filter(
            status=AlteracaoCardapio.workflow_class.CODAE_AUTORIZADO,
            escola__lote__in=self.lotes.all()
        )

    def alteracoes_cardapio_das_minhas_escolas_no_prazo_regular(self, filtro_aplicado):
        if filtro_aplicado == 'daqui_a_30_dias':
            alteracoes_cardapio = AlteracaoCardapio.prazo_regular_daqui_a_30_dias
        elif filtro_aplicado == 'daqui_a_7_dias':
            alteracoes_cardapio = AlteracaoCardapio.prazo_regular_daqui_a_7_dias
        else:
            alteracoes_cardapio = AlteracaoCardapio.prazo_regular
        return alteracoes_cardapio.filter(
            status=AlteracaoCardapio.workflow_class.CODAE_AUTORIZADO,
            escola__lote__in=self.lotes.all()
        )

    @property
    def alteracoes_cardapio_aprovadas(self):
        return AlteracaoCardapio.objects.filter(
            escola__lote__in=self.lotes.all(),
            status__in=[AlteracaoCardapio.workflow_class.CODAE_AUTORIZADO,
                        AlteracaoCardapio.workflow_class.TERCEIRIZADA_TOMA_CIENCIA]
        )

    @property
    def alteracoes_cardapio_reprovadas(self):
        return AlteracaoCardapio.objects.filter(
            escola__lote__in=self.lotes.all(),
            status=AlteracaoCardapio.workflow_class.CODAE_CANCELOU_PEDIDO
        )

    #
    # Inversão de dia de cardápio
    #

    def inversoes_cardapio_das_minhas_escolas(self, filtro_aplicado):
        if filtro_aplicado == 'daqui_a_7_dias':
            inversoes_cardapio = InversaoCardapio.prazo_limite_daqui_a_7_dias
        elif filtro_aplicado == 'daqui_a_30_dias':
            inversoes_cardapio = InversaoCardapio.prazo_limite_daqui_a_30_dias
        else:
            inversoes_cardapio = InversaoCardapio.objects
        return inversoes_cardapio.filter(
            escola__lote__in=self.lotes.all(),
            status=InversaoCardapio.workflow_class.CODAE_AUTORIZADO
        )

    @property
    def inversoes_cardapio_aprovadas(self):
        return InversaoCardapio.objects.filter(
            escola__lote__in=self.lotes.all(),
            status__in=[InversaoCardapio.workflow_class.CODAE_AUTORIZADO,
                        InversaoCardapio.workflow_class.TERCEIRIZADA_TOMA_CIENCIA]
        )

    #
    # Solicitação Unificada
    #

    def solicitacoes_unificadas_das_minhas_escolas(self, filtro_aplicado):
        if filtro_aplicado == 'daqui_a_7_dias':
            solicitacoes_unificadas = SolicitacaoKitLancheUnificada.prazo_limite_daqui_a_7_dias
        elif filtro_aplicado == 'daqui_a_30_dias':
            solicitacoes_unificadas = SolicitacaoKitLancheUnificada.prazo_limite_daqui_a_30_dias
        else:
            solicitacoes_unificadas = SolicitacaoKitLancheUnificada.objects
        return solicitacoes_unificadas.filter(
            escolas_quantidades__escola__lote__in=self.lotes.all(),
            status=SolicitacaoKitLancheUnificada.workflow_class.CODAE_AUTORIZADO
        ).distinct()

    @property
    def solicitacoes_unificadas_aprovadas(self):
        return SolicitacaoKitLancheUnificada.objects.filter(
            escolas_quantidades__escola__lote__in=self.lotes.all(),
            status__in=[SolicitacaoKitLancheUnificada.workflow_class.CODAE_AUTORIZADO,
                        SolicitacaoKitLancheUnificada.workflow_class.TERCEIRIZADA_TOMA_CIENCIA]
        ).distinct()

    def solicitacoes_kit_lanche_das_minhas_escolas_a_validar(self, filtro_aplicado):
        if filtro_aplicado == 'daqui_a_7_dias':
            solicitacoes_kit_lanche = SolicitacaoKitLancheAvulsa.prazo_limite_daqui_a_7_dias
        elif filtro_aplicado == 'daqui_a_30_dias':
            solicitacoes_kit_lanche = SolicitacaoKitLancheAvulsa.prazo_limite_daqui_a_30_dias
        else:
            solicitacoes_kit_lanche = SolicitacaoKitLancheAvulsa.objects
        return solicitacoes_kit_lanche.filter(
            escola__lote__in=self.lotes.all(),
            status=InversaoCardapio.workflow_class.CODAE_AUTORIZADO
        )

    def __str__(self):
        return f'{self.nome_fantasia}'

    class Meta:
        verbose_name = 'Terceirizada'
        verbose_name_plural = 'Terceirizadas'


class Contrato(TemChaveExterna):
    numero = models.CharField('No do contrato', max_length=100)
    processo = models.CharField('Processo Administrativo', max_length=100,
                                help_text='Processo administrativo do contrato')
    data_proposta = models.DateField('Data da proposta')
    lotes = models.ManyToManyField(Lote, related_name='contratos_do_lote')
    terceirizada = models.ForeignKey(Terceirizada, on_delete=models.CASCADE, related_name='contratos')
    edital = models.ForeignKey(Edital, on_delete=models.CASCADE, related_name='contratos', blank=True, null=True)
    diretorias_regionais = models.ManyToManyField(DiretoriaRegional, related_name='contratos_da_diretoria_regional')

    def __str__(self):
        return f'Contrato:{self.numero} Processo: {self.processo}'

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'


class VigenciaContrato(TemChaveExterna, IntervaloDeDia):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='vigencias', null=True, blank=True)

    def __str__(self):
        return f'Contrato:{self.contrato.numero} {self.data_inicial} a {self.data_final}'

    class Meta:
        verbose_name = 'Vigência de contrato'
        verbose_name_plural = 'Vigências de contrato'
