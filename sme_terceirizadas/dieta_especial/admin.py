from django.contrib import admin

from .models import (
    AlergiaIntolerancia,
    Anexo,
    ClassificacaoDieta,
    MotivoNegacao,
    SolicitacaoDietaEspecial,
    SubstituicaoAlimento
)

admin.site.register(AlergiaIntolerancia)
admin.site.register(Anexo)
admin.site.register(ClassificacaoDieta)
admin.site.register(MotivoNegacao)
admin.site.register(SolicitacaoDietaEspecial)
admin.site.register(SubstituicaoAlimento)
