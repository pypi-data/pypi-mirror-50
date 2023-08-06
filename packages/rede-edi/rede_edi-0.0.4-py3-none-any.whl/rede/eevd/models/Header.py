COLUMNS = (
    'TIPO_REGISTRO',
    'NRO_FILIAL_MATRIZ_GRUPO_COMERCIAO',
    'DT_EMISSAO',
    'DT_MOVIMENTO',
    'MOVIMENTACAO_DIARIA_CARTOES_DE_DEBITO',
    'REDE',
    'NOME_COMERCIAL_ESTABELECIMENTO',
    'SEQUENCIA_DE_MOVIMENTO',
    'TIPO_DE_PROCESSAMENTO',
    'VERSAO_ARQUIVO'
)

class EVDHeader:
    CONF = [
        (1, 2, '^[0-9]+$', 'TIPO_REGISTRO'),
        (2, 9, '^[0-9]+$', 'NRO_FILIAL_MATRIZ_GRUPO_COMERCIAO'),
        (3, 8, '^[0-9]+$', 'DT_EMISSAO (DDMMYYYY)'),
        (4, 8, '^[0-9]+$', 'DT_MOVIMENTO (DDMMYYYY)'),
        (5, 39, '^[a-zA-Z0-9]*$', 'MOVIMENTACAO DIARIA CARTOES DE DEBITO'),
        (6, 8, '^[a-zA-Z0-9]*$', 'REDE'),
        (7, 26, '^[a-zA-Z0-9]*$', 'NOME COMERCIAL DO ESTABELECIMENTO'),
        (8, 6, '^[0-9]+$', 'SEQUENCIA DE MOVIMENTO'),
        (9, 15, '^[a-zA-Z0-9]*$', 'TIPO DE PROCESSAMENTO (DIARIO/REPROCESSAMENTO)'),
        (10, 20, '^[a-zA-Z0-9]*$', 'Versão do arquivo (V1.04 – 07/10 –EEVD)')
    ]



def read(line):

    if not line.strip().endswith('EEVD'):
        return {}

    return dict(zip(COLUMNS, line.strip().split(',')))