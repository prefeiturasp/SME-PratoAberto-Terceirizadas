from django.contrib import admin

from .models import Alimento, Guia, SolicitacaoRemessa, TipoEmbalagem
from .services import inativa_tipos_de_embabalagem


class GuiaInline(admin.StackedInline):
    model = Guia
    extra = 1  # Quantidade de linhas que serão exibidas.
    show_change_link = True


class AlimentoInline(admin.TabularInline):
    model = Alimento
    extra = 1  # Quantidade de linhas que serão exibidas.


@admin.register(SolicitacaoRemessa)
class SolicitacaoAdmin(admin.ModelAdmin):

    def get_guias(self, obj):
        return ', '.join([
            guias.numero_guia for guias in obj.guias.all()
        ])
    get_guias.short_description = 'Guias'

    list_display = ('cnpj', 'numero_solicitacao', 'status', 'get_guias')
    ordering = ('-alterado_em',)
    search_fields = ('numero_solicitacao',)
    list_filter = ('status',)
    inlines = [GuiaInline]


@admin.register(Guia)
class GuiaAdmin(admin.ModelAdmin):

    def get_cnpj(self, obj):
        return obj.solicitacao.cnpj

    get_cnpj.short_description = 'CNPJ Armazem'

    def get_solicitacao(self, obj):
        return obj.solicitacao.numero_solicitacao
    get_solicitacao.short_description = 'Número Solicitação'

    def get_status_solicitacao(self, obj):
        return obj.solicitacao.get_status_display()
    get_status_solicitacao.short_description = 'Status da Solicitação'

    list_display = ('get_cnpj', 'get_solicitacao', 'get_status_solicitacao', 'numero_guia',
                    'data_entrega', 'codigo_unidade', 'nome_unidade', 'status')
    search_fields = ('numero_guia', 'solicitacao__numero_solicitacao', 'nome_unidade', 'codigo_unidade')
    list_filter = ('status',)
    ordering = ('-alterado_em',)
    inlines = [AlimentoInline]


@admin.register(TipoEmbalagem)
class TipoEmbalagemAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def get_tipo(self, obj):
        return f'{obj.sigla} - {obj.descricao}'

    get_tipo.short_description = 'Tipo de embalagem'

    def inativa_embalagens(self, request, queryset):
        inativa_tipos_de_embabalagem(queryset)
        self.message_user(request, 'Tipos de embalagens inativadas.')

    inativa_embalagens.short_description = 'Inativar Tipos de Embalagens'

    list_display = ('get_tipo',)
    actions = ['inativa_embalagens']
