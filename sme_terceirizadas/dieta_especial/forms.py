from django import forms

from ..escola.models import DiretoriaRegional, Escola
from .models import AlergiaIntolerancia, SolicitacaoDietaEspecial


class NegaDietaEspecialForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoDietaEspecial
        fields = [
            'justificativa_negacao',
            'motivo_negacao',
            'registro_funcional_nutricionista'
        ]


class SolicitacoesAtivasInativasPorAlunoForm(forms.Form):
    codigo_eol = forms.CharField(required=False)
    nome_aluno = forms.CharField(required=False)
    escola = forms.ModelChoiceField(
        required=False,
        queryset=Escola.objects.all(),
        to_field_name='uuid'
    )
    dre = forms.ModelChoiceField(
        required=False,
        queryset=DiretoriaRegional.objects.all(),
        to_field_name='uuid'
    )


class RelatorioQuantitativoSolicDietaEspForm(forms.Form):
    dre = forms.ModelMultipleChoiceField(
        required=False,
        queryset=DiretoriaRegional.objects.all(),
        to_field_name='uuid'
    )
    escola = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Escola.objects.all(),
        to_field_name='uuid'
    )
    diagnostico = forms.ModelMultipleChoiceField(
        required=False,
        queryset=AlergiaIntolerancia.objects.all()
    )
    status = forms.ChoiceField(required=False, choices=(
        ('', 'Todos'),
        ('ativas', 'Ativas'),
        ('inativas', 'Inativas'),
        ('pendentes', 'Pendentes'),
    ))
    data_inicial = forms.DateField(required=False)
    data_final = forms.DateField(required=False)
