import datetime

from rest_framework import serializers
from text_unidecode import unidecode

from ...dados_comuns.constants import DEZ_MB
from ...dados_comuns.utils import convert_base64_to_contentfile, convert_date_format, size
from ...dados_comuns.validators import deve_ser_no_passado, deve_ter_extensao_valida
from ...eol_servico.utils import EOLService
from ...escola.api.serializers import AlunoNaoMatriculadoSerializer
from ...escola.models import Aluno, Escola, PeriodoEscolar, Responsavel
from ...produto.models import Produto
from ..models import Anexo, SolicitacaoDietaEspecial, SubstituicaoAlimento
from .validators import AlunoSerializerValidator


class AnexoCreateSerializer(serializers.ModelSerializer):
    arquivo = serializers.CharField()
    nome = serializers.CharField()

    def validate_nome(self, nome):
        deve_ter_extensao_valida(nome)
        return nome

    class Meta:
        model = Anexo
        fields = ('arquivo', 'nome')


class SubstituicaoAlimentoCreateSerializer(serializers.ModelSerializer):
    substitutos = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Produto.objects.all(),
        many=True
    )

    class Meta:
        model = SubstituicaoAlimento
        fields = '__all__'


class SolicitacaoDietaEspecialCreateSerializer(serializers.ModelSerializer):
    anexos = serializers.ListField(
        child=AnexoCreateSerializer(), required=True
    )
    aluno_json = serializers.JSONField(required=False)
    aluno_nao_matriculado_data = AlunoNaoMatriculadoSerializer(required=False)
    aluno_nao_matriculado = serializers.BooleanField(default=False)

    def validate_anexos(self, anexos):
        for anexo in anexos:
            filesize = size(anexo['arquivo'])
            if filesize > DEZ_MB:
                raise serializers.ValidationError('O tamanho máximo de um arquivo é 10MB')
        if not anexos:
            raise serializers.ValidationError('Anexos não pode ser vazio')
        return anexos

    def validate_aluno_json(self, aluno_json):
        for value in ['codigo_eol', 'nome', 'data_nascimento']:
            if value not in aluno_json:
                raise serializers.ValidationError(f'deve ter atributo {value}')
        validator = AlunoSerializerValidator(data=aluno_json)
        if validator.is_valid():
            return aluno_json
        else:
            raise serializers.ValidationError(f'{validator.errors}')

    def create(self, validated_data):  # noqa C901
        validated_data['criado_por'] = self.context['request'].user
        anexos = validated_data.pop('anexos', [])
        aluno_data = validated_data.pop('aluno_json', None)
        aluno_nao_matriculado_data = validated_data.pop('aluno_nao_matriculado_data', None)
        aluno_nao_matriculado = validated_data.pop('aluno_nao_matriculado')

        if aluno_nao_matriculado:
            aluno = aluno_nao_matriculado_data
            codigo_eol_escola = aluno_nao_matriculado_data.pop('codigo_eol_escola')
            responsavel_data = aluno_nao_matriculado_data.pop('responsavel')
            cpf_aluno = aluno_nao_matriculado_data.get('cpf')
            nome_aluno = aluno_nao_matriculado_data.get('nome')
            data_nascimento = aluno_nao_matriculado_data.get('data_nascimento')

            escola = Escola.objects.get(codigo_eol=codigo_eol_escola)

            aluno = Aluno.objects.filter(nome__iexact=nome_aluno, responsaveis__cpf=responsavel_data.get('cpf')).last()

            if cpf_aluno and not aluno:
                aluno, _ = Aluno.objects.get_or_create(
                    cpf=cpf_aluno,
                    defaults={'nome': nome_aluno, 'data_nascimento': data_nascimento}
                )
            elif not aluno:
                aluno = Aluno.objects.create(nome=nome_aluno, data_nascimento=data_nascimento)

            if SolicitacaoDietaEspecial.aluno_possui_dieta_especial_pendente(aluno):
                raise serializers.ValidationError('Aluno já possui Solicitação de Dieta Especial pendente')

            aluno.escola = escola
            aluno.nao_matriculado = True
            aluno.save()

            responsavel, _ = Responsavel.objects.get_or_create(
                cpf=responsavel_data.get('cpf'),
                defaults={'nome': responsavel_data.get('nome')}
            )
            aluno.responsaveis.add(responsavel)

        else:
            info_turma = EOLService.get_informacoes_escola_turma_aluno(
                validated_data['criado_por'].vinculo_atual.instituicao.codigo_eol)
            for registro in info_turma:
                if registro['cd_aluno'] == int(aluno_data['codigo_eol']):
                    periodo_nome = registro['dc_tipo_turno']
                    break
            else:
                raise serializers.ValidationError('Aluno não pertence a essa escola')

            aluno = self._get_or_create_aluno(aluno_data)

            if SolicitacaoDietaEspecial.aluno_possui_dieta_especial_pendente(aluno):
                raise serializers.ValidationError('Aluno já possui Solicitação de Dieta Especial pendente')

            periodo = PeriodoEscolar.objects.get(nome__icontains=unidecode(periodo_nome.strip()))
            aluno.escola = validated_data['criado_por'].vinculo_atual.instituicao
            aluno.periodo_escolar = periodo
            aluno.save()

        solicitacao = SolicitacaoDietaEspecial.objects.create(**validated_data)
        solicitacao.aluno = aluno
        solicitacao.ativo = False
        solicitacao.save()

        for anexo in anexos:
            data = convert_base64_to_contentfile(anexo.get('arquivo'))
            Anexo.objects.create(
                solicitacao_dieta_especial=solicitacao,
                arquivo=data,
                nome=anexo.get('nome', '')
            )

        solicitacao.inicia_fluxo(user=self.context['request'].user)
        return solicitacao

    def _get_or_create_aluno(self, aluno_data):
        escola = self.context['request'].user.vinculo_atual.instituicao
        codigo_eol_aluno = aluno_data.get('codigo_eol')
        nome_aluno = aluno_data.get('nome')
        data_nascimento_aluno = convert_date_format(
            date=aluno_data.get('data_nascimento'),
            from_format='%d/%m/%Y',
            to_format='%Y-%m-%d'
        )
        deve_ser_no_passado(datetime.datetime.strptime(data_nascimento_aluno, '%Y-%m-%d').date())
        try:
            aluno = Aluno.objects.get(codigo_eol=codigo_eol_aluno)
        except Aluno.DoesNotExist:
            aluno = Aluno(codigo_eol=codigo_eol_aluno,
                          nome=nome_aluno,
                          data_nascimento=data_nascimento_aluno,
                          escola=escola)
            aluno.save()
        return aluno

    class Meta:
        model = SolicitacaoDietaEspecial
        fields = (
            'aluno_json',
            'uuid',
            'nome_completo_pescritor',
            'registro_funcional_pescritor',
            'observacoes',
            'criado_em',
            'anexos',
            'aluno_nao_matriculado',
            'aluno_nao_matriculado_data'
        )
