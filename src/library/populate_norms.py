"""Script para popular a biblioteca com normas brasileiras"""

from pathlib import Path
from .norms_library import NormsLibrary


def populate_norms(db_path: Path):
    """Popula banco de dados com normas brasileiras relevantes"""
    library = NormsLibrary(db_path)

    # NR-6: Equipamento de Proteção Individual
    library.add_norm(
        "NR-6",
        "Norma Regulamentadora nº 6 - Equipamento de Proteção Individual (EPI)",
        "Establece os requisitos e responsabilidades para o fornecimento, uso e manutenção de EPI",
        "Atualizada 2023",
        "1978"
    )

    library.add_content(
        "NR-6",
        "Artigo 1",
        "Art. 1º",
        """A empresa é obrigada a fornecer aos empregados, gratuitamente, EPI adequado ao risco, em
        perfeito estado de conservação e funcionamento, nas seguintes circunstâncias: sempre que as medidas de
        proteção coletiva forem tecnicamente inviáveis ou insuficientes para eliminar ou reduzir os riscos;
        enquanto estão sendo implantadas medidas de proteção coletiva; para atender a situações de emergência."""
    )

    library.add_content(
        "NR-6",
        "Artigo 2",
        "Art. 2º",
        """O equipamento de proteção individual será selecionado levando-se em consideração sua eficácia,
        o conforto do usuário e a compatibilidade entre si. Todos os EPI devem conter a indicação de seu tipo,
        o número deste Anexo, o ano de fabricação e o número do lote de fabricação. Os EPI devem ter validade
        conforme disposto nas instruções técnicas de cada tipo de equipamento."""
    )

    library.add_content(
        "NR-6",
        "Certificação",
        "CA",
        """O EPI só pode ser considerado apto para comercialização e uso quando dispor de
        Certificado de Aprovação (CA) expedido pelo Ministério do Trabalho e Emprego. O CA é obtido através
        de inspeção e testes específicos realizados em laboratórios acreditados. A validade do CA é de 5 anos."""
    )

    # NR-10: Segurança em Instalações e Serviços com Eletricidade
    library.add_norm(
        "NR-10",
        "Norma Regulamentadora nº 10 - Segurança em Instalações e Serviços com Eletricidade",
        "Estabelece os requisitos e condições mínimas objetivando a implementação de medidas de controle",
        "Atualizada 2023",
        "2004"
    )

    library.add_content(
        "NR-10",
        "Objetivo",
        "Art. 1º",
        """Esta Norma Regulamentadora estabelece os requisitos e condições mínimas para que o trabalho
        em instalações elétricas seja realizado com segurança. As medidas de controle incluem:
        desenergização, aterramento, equipotencialização e dispositivos de proteção."""
    )

    # NR-12: Segurança do Trabalho em Máquinas e Equipamentos
    library.add_norm(
        "NR-12",
        "Norma Regulamentadora nº 12 - Segurança do Trabalho em Máquinas e Equipamentos",
        "Estabelece métodos e critérios para a promoção de saúde e segurança no trabalho em máquinas",
        "Atualizada 2023",
        "1978"
    )

    library.add_content(
        "NR-12",
        "Proteção",
        "Art. 1º",
        """Toda máquina ou equipamento deve possuir sistema de proteção adequado à sua periculosidade.
        As proteções devem ser projetadas e construídas para prevenir o acesso às zonas de perigo durante
        o funcionamento normal da máquina. Os dispositivos de proteção devem ser resistentes, durável e de
        difícil remoção."""
    )

    library.add_content(
        "NR-12",
        "Parada",
        "Art. 2º",
        """Toda máquina deve dispor de dispositivos de parada que permitam a desenergização da força
        motora. Os botões de parada devem estar localizados em posição facilmente acessível ao operador.
        É obrigatória a instalação de dois botões de parada independentes em máquinas com estrutura grande."""
    )

    # NR-15: Atividades e Operações Insalubres
    library.add_norm(
        "NR-15",
        "Norma Regulamentadora nº 15 - Atividades e Operações Insalubres",
        "Define atividades insalubres e estabelece limites de tolerância para agentes nocivos",
        "Atualizada 2023",
        "1978"
    )

    library.add_content(
        "NR-15",
        "Insalubridade",
        "Art. 1º",
        """Serão consideradas atividades ou operações insalubres aquelas que, por sua natureza,
        condições ou métodos de trabalho, exponham os empregados a agentes nocivos à saúde, acima dos
        limites de tolerância fixados em relação com a natureza e a intensidade do agente e o tempo de
        exposição aos seus efeitos. A caracterização da insalubridade de uma atividade ou operação dependerá
        da verificação dos níveis de concentração ou intensidade do agente nocivo."""
    )

    library.add_content(
        "NR-15",
        "Ruído",
        "Anexo 1",
        """O Limite de Tolerância para ruído contínuo ou intermitente é de 85 dB(A) para 8 horas diárias.
        Para ruído de impacto, o Limite de Tolerância é de 130 dB(C). A exposição ao ruído acima de 85 dB(A)
        obriga o uso de protetor auricular. Para níveis entre 80 e 85 dB(A), recomenda-se proteção."""
    )

    library.add_content(
        "NR-15",
        "Temperatur",
        "Anexo 3",
        """Os trabalhos em ambientes quentes devem ser realizados de forma a prevenir a fadiga por calor.
        Para calor radiante, a temperatura não deve exceder certos limites. O trabalho intermitente em ambientes
        quentes requer pausas em ambientes frescos. A exposição excessiva ao calor pode causar golpe de calor,
        desidratação e fadiga."""
    )

    # NR-17: Ergonomia
    library.add_norm(
        "NR-17",
        "Norma Regulamentadora nº 17 - Ergonomia",
        "Estabelece parâmetros que permitem a adaptação das condições de trabalho às características fisiológicas",
        "Atualizada 2023",
        "1990"
    )

    library.add_content(
        "NR-17",
        "Objetivo",
        "Art. 1º",
        """Esta Norma visa estabelecer parâmetros que permitem a adaptação das condições de trabalho
        às características psicofisiológicas dos trabalhadores, de modo a proporcionar conforto, segurança e
        desempenho eficiente. Os parâmetros da norma envolvem postura, mobiliário, organização do trabalho,
        levantamento de cargas e ambiente."""
    )

    library.add_content(
        "NR-17",
        "Postura",
        "Art. 2º",
        """O trabalho deve ser realizado de forma a garantir a postura adequada do trabalhador.
        A altura do assento da cadeira deve ser ajustável, permitindo que os pés fiquem apoiados no chão com
        as pernas em ângulo de 90 graus aproximadamente. O encosto deve ter altura entre 30 e 40 cm e inclinação
        entre 90 e 110 graus. A profundidade do assento deve ter entre 40 e 50 cm."""
    )

    library.add_content(
        "NR-17",
        "Levantamento",
        "Art. 3º",
        """Para levantamento, transporte e descarga de materiais, deve-se observar os seguintes limites
        de peso: máximo de 20 kg para mulheres; máximo de 25 kg para homens. Para crianças e adolescentes,
        o limite é menor conforme a idade. Deve-se também considerar a frequência, distância vertical, assimetria
        na posição do corpo e acoplamento com a carga."""
    )

    library.add_content(
        "NR-17",
        "Organização",
        "Art. 4º",
        """A organização do trabalho deve ser adequada às características psicofisiológicas dos trabalhadores.
        Devem ser observados os seguintes itens: pausas e períodos de descanso; alternância de atividades;
        ritmo de trabalho compatível com a capacidade do trabalhador; consideração de aspectos psicossociais do trabalho."""
    )

    # NR-32: Segurança e Saúde no Trabalho em Estabelecimentos de Saúde
    library.add_norm(
        "NR-32",
        "Norma Regulamentadora nº 32 - Segurança e Saúde no Trabalho em Estabelecimentos de Saúde",
        "Estabelece diretrizes de implementação de medidas de proteção à segurança e saúde dos trabalhadores",
        "Atualizada 2023",
        "2005"
    )

    library.add_content(
        "NR-32",
        "Objetivo",
        "Art. 1º",
        """Esta Norma estabelece diretrizes para implementação de medidas de proteção à segurança e saúde
        dos trabalhadores dos serviços de saúde, bem como daqueles que exercem atividades de promoção e
        assistência à saúde em geral. Abrange exposição a sangue, fluidos corpóreos, aerossóis e agentes biológicos."""
    )

    # ISO 31010
    library.add_norm(
        "ISO-31010",
        "ISO 31010:2019 - Risk Management - Risk Assessment Techniques",
        "Fornece orientações para a seleção e aplicação de técnicas de avaliação de riscos",
        "2019",
        "2019"
    )

    library.add_content(
        "ISO-31010",
        "Escopo",
        "Artigo 1",
        """Esta norma fornece orientação para a seleção e aplicação de técnicas de avaliação de risco.
        Ela reconhece que existem várias técnicas disponíveis e que diferentes técnicas são apropriadas para
        diferentes situações. A matriz de risco usando severidade versus probabilidade é uma abordagem comum
        para representar os resultados da avaliação de risco de forma visual."""
    )

    library.add_content(
        "ISO-31010",
        "Matriz",
        "Artigo 2",
        """A matriz de risco combina a avaliação da probabilidade de ocorrência de um evento com a
        avaliação da severidade de suas consequências. A escala de severidade pode incluir: insignificante,
        menor, moderado, maior, catastrófico. A escala de probabilidade pode incluir: raro, improvável,
        possível, provável, muito provável. O nível final de risco é determinado pela intersecção destas dimensões."""
    )

    print("✅ Banco de dados populado com sucesso!")
    stats = library.get_statistics()
    print(f"   - {stats['total_norms']} normas")
    print(f"   - {stats['total_articles']} artigos/seções")
    print(f"   - ~{stats['total_words']:,} palavras indexadas")
