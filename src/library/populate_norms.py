"""Script para popular a biblioteca com normas brasileiras com datas reais"""

from pathlib import Path
from .norms_library import NormsLibrary


def populate_norms(db_path: Path):
    """Popula banco de dados com normas brasileiras relevantes"""
    library = NormsLibrary(db_path)

    # ===== NR-1: Disposições Gerais =====
    library.add_norm(
        "NR-1",
        "Norma Regulamentadora nº 1 - Disposições Gerais",
        "Estabelece as disposições gerais que se aplicam a todas as atividades econômicas.",
        "1.9.1",
        "1978-06-08",
        "2023-03-15"
    )

    library.add_content("NR-1", "Objetivo", "Art. 1º",
        """Esta Norma Regulamentadora estabelece as disposições gerais que se aplicam a todas as
        atividades econômicas cobertas pela Lei nº 6.514, de 22 de dezembro de 1977, excetuadas as
        Atividades em Regime de Trabalho no Domicílio e as Atividades Leiloeiras. O objetivo é promover
        a saúde e segurança dos trabalhadores do país.""")

    library.add_content("NR-1", "Obrigações", "Art. 2º",
        """Cabe ao empregador cumprir e fazer cumprir as disposições legais, regulamentares e normativas
        sobre segurança, higiene e medicina do trabalho. Os empregadores devem informar aos empregados,
        através de avisos afixados em locais visíveis, sobre os riscos profissionais que comportam a
        atividade exercida e as medidas de prevenção e proteção adotadas.""")

    library.add_content("NR-1", "SESMT", "Art. 3º",
        """Os Serviços de Saúde do Trabalhador nas empresas de grau de risco 3 e 4, com 100 ou mais
        empregados, e nas empresas de grau de risco 1 e 2, com 500 ou mais empregados, deverão manter
        Médico do Trabalho como responsável técnico. O Médico do Trabalho realizará avaliações clínicas
        dos trabalhadores em função dos riscos a que estão expostos.""")

    library.add_content("NR-1", "CIPA", "Art. 4º",
        """A Comissão Interna de Prevenção de Acidentes - CIPA será obrigatória nas empresas ou
        estabelecimentos que possuam 20 ou mais empregados. A CIPA terá por atribuição, entre outras,
        a investigação de acidentes, incidentes e doenças do trabalho, bem como a formação de grupos
        de trabalho que deliberem sobre o conhecimento dos riscos profissionais.""")

    # ===== NR-6: Equipamento de Proteção Individual =====
    library.add_norm(
        "NR-6",
        "Norma Regulamentadora nº 6 - Equipamento de Proteção Individual (EPI)",
        "Establece os requisitos e responsabilidades para fornecimento, uso e manutenção de EPI",
        "1.10",
        "1978-06-08",
        "2020-11-11"
    )

    library.add_content("NR-6", "Definição", "Art. 1º",
        """Equipamento de Proteção Individual - EPI é todo dispositivo ou produto de uso individual
        destinado a proteger a saúde e a integridade física do trabalhador. Considerando-se de uso
        individual os equipamentos de proteção que se destinam a proteger um único trabalhador.""")

    library.add_content("NR-6", "Fornecimento", "Art. 2º",
        """A empresa é obrigada a fornecer aos empregados, gratuitamente, EPI adequado ao risco,
        em perfeito estado de conservação e funcionamento. Sempre que as medidas de proteção coletiva
        forem tecnicamente inviáveis ou insuficientes para eliminar ou reduzir os riscos.""")

    library.add_content("NR-6", "Certificação", "Art. 3º",
        """O EPI só pode ser considerado apto para comercialização e uso quando dispuser de
        Certificado de Aprovação (CA) expedido pelo Ministério do Trabalho. O CA é obtido através
        de inspeção e testes específicos realizados em laboratórios acreditados. A validade do CA
        é de 5 anos.""")

    library.add_content("NR-6", "Categorias", "Art. 4º",
        """Os EPIs se classificam em categorias: Proteção da Cabeça (capacetes); Proteção dos Olhos
        (óculos, protetores faciais); Proteção Auditiva (protetores auriculares); Proteção Respiratória
        (máscaras, respiradores); Proteção do Tronco (aventais, coletes); Proteção de Membros Superiores
        (luvas); Proteção de Membros Inferiores e Pés (botas, sapatos).""")

    # ===== NR-10: Segurança em Eletricidade =====
    library.add_norm(
        "NR-10",
        "Norma Regulamentadora nº 10 - Segurança em Instalações e Serviços com Eletricidade",
        "Estabelece os requisitos para trabalho seguro com eletricidade",
        "1.7.1",
        "2004-12-08",
        "2021-04-20"
    )

    library.add_content("NR-10", "Objetivo", "Art. 1º",
        """Esta Norma Regulamentadora estabelece os requisitos e condições mínimas para que o trabalho
        em instalações elétricas seja realizado com segurança. As medidas de controle incluem a
        desenergização, aterramento, equipotencialização e dispositivos de proteção contra contatos
        diretos e indiretos.""")

    library.add_content("NR-10", "Desenergização", "Art. 2º",
        """Desenergizar equipamentos é uma medida de controle de risco implementada isoladamente ou
        em conjunto com outras medidas de proteção para garantir a segurança. A desenergização
        aplica-se a qualquer atividade em instalações elétricas como: construção, manutenção,
        inspeção, reforma, ampliação, restauração.""")

    library.add_content("NR-10", "Treinamento", "Art. 3º",
        """O trabalhador autorizado que intervenha em instalações elétricas energizadas deve participar
        de treinamento de segurança em instalações elétricas. Todo trabalhador que intervenha em
        instalações elétricas deve ser instruído e treinado com documentação comprovada, de tal forma
        que demonstre capacidade para trabalhar com segurança.""")

    library.add_content("NR-10", "Equipamento", "Art. 4º",
        """Os trabalhos em instalações elétricas exigem equipamento de proteção individual apropriado.
        Tais como: capacete com resistência a penetração de objetos e comportamento diante de energias
        elétrica; óculos de segurança; luvas de borracha ou outro material equivalente; calçado de
        segurança; roupa apropriada sem materiais que facilitam combustão.""")

    # ===== NR-12: Segurança em Máquinas =====
    library.add_norm(
        "NR-12",
        "Norma Regulamentadora nº 12 - Segurança do Trabalho em Máquinas e Equipamentos",
        "Estabelece métodos e critérios para a promoção de saúde e segurança no trabalho em máquinas",
        "1.7",
        "1978-06-08",
        "2022-01-20"
    )

    library.add_content("NR-12", "Zonas de Perigo", "Art. 1º",
        """Toda máquina ou equipamento deve possuir sistema de proteção adequado à sua periculosidade.
        As proteções devem ser projetadas e construídas para prevenir o acesso às zonas de perigo
        durante o funcionamento normal da máquina. Os dispositivos de proteção devem ser resistentes,
        duráveis e de difícil remoção.""")

    library.add_content("NR-12", "Parada de Emergência", "Art. 2º",
        """Toda máquina deve dispor de dispositivos de parada que permitam a desenergização da força
        motora. Os botões de parada devem estar localizados em posição facilmente acessível ao operador.
        É obrigatória a instalação de dois botões de parada independentes em máquinas com estrutura grande.""")

    library.add_content("NR-12", "Manutenção", "Art. 3º",
        """A manutenção das máquinas deve ser realizada de forma a garantir as condições de segurança.
        Os trabalhos de ajuste, limpeza, reparação e substituição de partes devem ser realizados com
        a máquina parada, exceto nos casos em que for imprescindível o seu funcionamento.""")

    library.add_content("NR-12", "Dispositivos", "Art. 4º",
        """As máquinas devem estar dotadas de sistemas de proteção por encapsulamento, enclausuramentos,
        blindagens, barreiras, anteparos, ou outros dispositivos apropriados. Todos os restos de máquinas
        que ofereçam risco deverão ser resguardados.""")

    # ===== NR-15: Atividades Insalubres =====
    library.add_norm(
        "NR-15",
        "Norma Regulamentadora nº 15 - Atividades e Operações Insalubres",
        "Define atividades insalubres e estabelece limites de tolerância para agentes nocivos",
        "1.7",
        "1978-06-08",
        "2023-02-08"
    )

    library.add_content("NR-15", "Definição", "Art. 1º",
        """Serão consideradas atividades ou operações insalubres aquelas que, por sua natureza,
        condições ou métodos de trabalho, exponham os empregados a agentes nocivos à saúde, acima dos
        limites de tolerância fixados em relação com a natureza e a intensidade do agente e o tempo de
        exposição aos seus efeitos.""")

    library.add_content("NR-15", "Ruído - Limite", "Anexo 1",
        """O Limite de Tolerância para ruído contínuo ou intermitente, medido em decibel (dB), segundo
        a escala A de ponderação, é de 85 dB(A) para uma exposição de 8 horas diárias. Para ruído de
        impacto, o Limite de Tolerância é de 130 dB(C). A exposição ao ruído acima de 85 dB(A) obriga
        o uso de protetor auricular adequado.""")

    library.add_content("NR-15", "Temperatura", "Anexo 3",
        """Os trabalhos em ambientes quentes devem ser realizados de forma a prevenir a fadiga por
        calor, transtornos causados pelo calor e, em particular, o golpe de calor. O trabalho intermitente
        em ambientes quentes requer pausas em ambientes frescos. A exposição excessiva ao calor pode
        causar golpe de calor, desidratação e fadiga.""")

    library.add_content("NR-15", "Radiação Ionizante", "Anexo 5",
        """Qualquer exposição à radiação ionizante é prejudicial à saúde. O limite anual de dose
        para trabalhadores ocupacionalmente expostos é de 20 mSv em qualquer ano. As práticas de
        proteção radiológica devem ser baseadas no princípio ALARA: As Low As Reasonably Achievable.""")

    library.add_content("NR-15", "Agentes Biológicos", "Anexo 7",
        """Os trabalhadores podem estar expostos a agentes biológicos como bactérias, vírus, fungos,
        parasitos e seus produtos. As atividades com risco biológico requerem vigilância médica, uso
        de EPI apropriado e medidas de controle de infecção.""")

    # ===== NR-17: Ergonomia =====
    library.add_norm(
        "NR-17",
        "Norma Regulamentadora nº 17 - Ergonomia",
        "Estabelece parâmetros que permitem a adaptação das condições de trabalho às características fisiológicas",
        "1.7.1",
        "1990-11-29",
        "2022-05-23"
    )

    library.add_content("NR-17", "Objetivo", "Art. 1º",
        """Esta Norma visa estabelecer parâmetros que permitem a adaptação das condições de trabalho
        às características psicofisiológicas dos trabalhadores, de modo a proporcionar conforto, segurança
        e desempenho eficiente. Os parâmetros da norma envolvem postura, mobiliário, organização do
        trabalho, levantamento de cargas e ambiente.""")

    library.add_content("NR-17", "Postura - Cadeira", "Art. 2º",
        """O trabalho deve ser realizado de forma a garantir a postura adequada do trabalhador.
        A altura do assento da cadeira deve ser ajustável, permitindo que os pés fiquem apoiados no chão
        com as pernas em ângulo de 90 graus aproximadamente. O encosto deve ter altura entre 30 e 40 cm
        e inclinação entre 90 e 110 graus. A profundidade do assento deve ter entre 40 e 50 cm.""")

    library.add_content("NR-17", "Levantamento Manual", "Art. 3º",
        """Para levantamento, transporte e descarga de materiais, deve-se observar os seguintes limites
        de peso: máximo de 20 kg para mulheres; máximo de 25 kg para homens. Para crianças e adolescentes,
        o limite é menor conforme a idade. Deve-se também considerar a frequência, distância vertical,
        assimetria na posição do corpo e acoplamento com a carga.""")

    library.add_content("NR-17", "Organização", "Art. 4º",
        """A organização do trabalho deve ser adequada às características psicofisiológicas dos
        trabalhadores. Devem ser observados os seguintes itens: pausas e períodos de descanso;
        alternância de atividades; ritmo de trabalho compatível com a capacidade do trabalhador;
        consideração de aspectos psicossociais do trabalho.""")

    library.add_content("NR-17", "Ambiente", "Art. 5º",
        """A norma regulamenta a iluminação, temperatura e umidade dos ambientes de trabalho.
        A iluminação deve ser adequada ao tipo de atividade: 150 lux para ambientes com tarefas simples,
        300 lux para tarefas normais, 500 lux para tarefas de precisão. A temperatura deve estar entre
        20ºC e 23ºC, com umidade relativa entre 40% e 60%.""")

    # ===== NR-18: Segurança na Construção =====
    library.add_norm(
        "NR-18",
        "Norma Regulamentadora nº 18 - Segurança e Saúde do Trabalho na Indústria da Construção",
        "Estabelece diretrizes de segurança para trabalhos em construção",
        "1.9.1",
        "1978-06-08",
        "2020-07-21"
    )

    library.add_content("NR-18", "Objetivo", "Art. 1º",
        """Esta Norma Regulamentadora estabelece diretrizes sobre proteção da segurança, da saúde e do
        meio ambiente para os trabalhadores envolvidos, direta ou indiretamente, nas atividades de construção,
        compreendendo entre outros: o projeto, a fabricação de componentes e estruturas, o transporte, a
        descarga, a armazenagem e a montagem de estruturas.""")

    library.add_content("NR-18", "Queda em Altura", "Art. 2º",
        """O trabalho em altura deve ser precedido de análise de risco e implementação de medidas de
        proteção específicas. Todos os trabalhadores que realizam trabalho em altura devem usar cintos de
        segurança, talabarte e outros equipamentos apropriados. A altura mínima para exigência de proteção
        é de 2 metros.""")

    library.add_content("NR-18", "Andaimes", "Art. 3º",
        """Os andaimes devem ser construídos, mantidos e utilizados de forma que seja mantida sua
        estabilidade e resistência. Os andaimes deverão ter capacidade de carga de no mínimo 4 vezes o peso
        máximo de pessoas, ferramentas e materiais que nele serão colocados.""")

    library.add_content("NR-18", "Proteção de Abertura", "Art. 4º",
        """Toda abertura no piso deve ser protegida contra quedas de pessoas ou objetos. As proteções
        devem ser feitas com gradil de altura mínima de 1,20 m ou tela de arame resistente. Para aberturas
        quadradas ou retangulares com lado menor superior a 0,15 m, deve-se tomar providências.""")

    # ===== NR-31: Segurança na Agricultura =====
    library.add_norm(
        "NR-31",
        "Norma Regulamentadora nº 31 - Segurança e Saúde do Trabalho na Agricultura, Pecuária e Floresta",
        "Estabelece diretrizes para segurança em atividades agrícolas",
        "1.8.1",
        "2004-04-08",
        "2020-05-29"
    )

    library.add_content("NR-31", "Objetivo", "Art. 1º",
        """Esta Norma Regulamentadora estabelece diretrizes para implementação de medidas de proteção à
        segurança e saúde dos trabalhadores dos serviços de agricultura, pecuária, silvicultura e exploração
        florestal. Abrange proteção contra agentes químicos, biológicos, físicos e de organização do trabalho.""")

    library.add_content("NR-31", "Agrotóxicos", "Art. 2º",
        """O uso de agrotóxicos deve ser realizado com segurança. O empregador deve disponibilizar
        equipamento de proteção individual apropriado para cada trabalhador. Os agrotóxicos devem ser
        aplicados de forma a evitar contato com o corpo do aplicador, considerando-se especialmente o
        rosto, as mãos e os pés.""")

    library.add_content("NR-31", "Máquinas Agrícolas", "Art. 3º",
        """As máquinas agrícolas devem estar adequadamente protegidas. Motores de combustão interna devem
        ser equipados com silenciador e proteção contra queimaduras. As máquinas devem ter proteção contra
        partes móveis, cintas, correntes e engrenagens.""")

    library.add_content("NR-31", "Animais", "Art. 4º",
        """Na manipulação de animais deve-se implementar medidas de prevenção e proteção. Os trabalhadores
        devem receber treinamento sobre manejo de animais e uso de equipamentos de segurança apropriados.
        As instalações para confinamento de animais devem ser projetadas com segurança.""")

    # ===== NR-32: Segurança em Estabelecimentos de Saúde =====
    library.add_norm(
        "NR-32",
        "Norma Regulamentadora nº 32 - Segurança e Saúde no Trabalho em Estabelecimentos de Saúde",
        "Estabelece diretrizes para segurança em serviços de saúde",
        "1.8.1",
        "2005-12-16",
        "2023-01-27"
    )

    library.add_content("NR-32", "Objetivo", "Art. 1º",
        """Esta Norma estabelece diretrizes para implementação de medidas de proteção à segurança e saúde
        dos trabalhadores dos serviços de saúde, bem como daqueles que exercem atividades de promoção e
        assistência à saúde em geral. Abrange exposição a sangue, fluidos corpóreos, aerossóis e agentes
        biológicos.""")

    library.add_content("NR-32", "Exposição Biológica", "Art. 2º",
        """Qualquer exposição a sangue ou fluidos corpóreos deve ser considerada como exposição a material
        biológico potencialmente infeccioso. Todos os trabalhadores devem usar Equipamento de Proteção
        Individual apropriado para sua atividade. A exposição ocupacional a agentes biológicos implica risco
        de infecção.""")

    library.add_content("NR-32", "Acidente com Biológico", "Art. 3º",
        """Todo acidente que envolva exposição a material biológico deve ser comunicado e investigado.
        O trabalhador acidentado deve receber atendimento médico imediato. Deve ser fornecido soroterapia
        e vacinação quando indicado, conforme protocolos estabelecidos.""")

    library.add_content("NR-32", "Resíduos", "Art. 4º",
        """Os resíduos gerados nos serviços de saúde que apresentam risco biológico devem ser segregados
        e acondicionados adequadamente. O armazenamento temporário não deve exceder 48 horas em clima
        ameno ou 72 horas em clima frio. Os resíduos biológicos devem ser tratados antes da disposição final.""")

    # ===== NR-36: Segurança em Abate =====
    library.add_norm(
        "NR-36",
        "Norma Regulamentadora nº 36 - Segurança e Saúde do Trabalho em Empresas de Abate e Processamento de Carnes",
        "Estabelece diretrizes para segurança em plantas de abate e processamento",
        "1.1",
        "2013-03-15",
        "2020-12-16"
    )

    library.add_content("NR-36", "Objetivo", "Art. 1º",
        """Esta Norma Regulamentadora estabelece diretrizes para implementação de medidas de proteção à
        segurança e saúde dos trabalhadores nas empresas de abate e processamento de carnes. Abrange proteção
        contra agentes físicos, químicos, biológicos, ergonômicos e de organização do trabalho.""")

    library.add_content("NR-36", "Temperatura", "Art. 2º",
        """As atividades de processamento em ambientes frios exigem medidas de proteção específicas. Os
        trabalhadores que realizam atividades em temperaturas muito baixas devem usar equipamentos de proteção
        adequados. Devem ser fornecidas pausas em ambientes aquecidos ou locais apropriados para aquecimento.""")

    library.add_content("NR-36", "Equipamento de Corte", "Art. 3º",
        """Os equipamentos de corte e descamação devem possuir proteção específica para evitar acidentes.
        As facas e equipamentos similares devem ser mantidos afiados para reduzir a força necessária ao corte.
        Os utensílios de corte devem ser armazenados de forma segura quando não utilizados.""")

    library.add_content("NR-36", "Lesão por Esforço Repetitivo", "Art. 4º",
        """As atividades de processamento envolvem movimentos repetitivos que podem causar lesão por
        esforço repetitivo. Devem ser implementadas medidas de prevenção como: alternância de atividades,
        pausas para descanso, ginástica laboral, adequação ergonômica do local de trabalho.""")

    # ===== ISO 31010: Técnicas de Avaliação de Risco =====
    library.add_norm(
        "ISO-31010",
        "ISO 31010:2019 - Risk Management - Risk Assessment Techniques",
        "Fornece orientações para seleção e aplicação de técnicas de avaliação de riscos",
        "2019",
        "2019-02-15",
        "2019-02-15"
    )

    library.add_content("ISO-31010", "Escopo", "1 Scope",
        """Esta norma fornece orientação para a seleção e aplicação de técnicas de avaliação de risco.
        Ela reconhece que existem várias técnicas disponíveis e que diferentes técnicas são apropriadas para
        diferentes situações. A abordagem deve ser sistemática, metodológica e bem documentada.""")

    library.add_content("ISO-31010", "Matriz de Risco", "4.4 Risk Matrix",
        """A matriz de risco combina a avaliação da probabilidade de ocorrência com a avaliação da
        severidade de suas consequências. A escala de severidade pode incluir: insignificante, menor, moderado,
        maior, catastrófico. A escala de probabilidade pode incluir: raro, improvável, possível, provável,
        muito provável. O nível final de risco é determinado pela intersecção destas dimensões.""")

    library.add_content("ISO-31010", "Análise de Modo de Falha", "5.3 FMEA",
        """Failure Mode and Effects Analysis (FMEA) é uma técnica sistemática para avaliar o impacto
        potencial de falhas. Para cada modo de falha identificado, avalia-se a severidade do efeito, a
        probabilidade de ocorrência e a detectabilidade. O Índice de Prioridade de Risco (RPN) é calculado
        como o produto desses três fatores.""")

    library.add_content("ISO-31010", "Análise de Árvore de Falhas", "5.4 FTA",
        """Fault Tree Analysis (FTA) é uma técnica dedutiva que começa com um evento indesejável e
        trabalha para trás através dos subsistemas e componentes para identificar as causas raiz. A árvore
        de falhas é representada graficamente mostrando as relações lógicas entre eventos básicos e intermediários.""")

    library.add_content("ISO-31010", "Check-list", "5.5 Checklists",
        """Check-lists são ferramentas simples e eficazes para avaliação de riscos baseadas em experiência
        anterior. Uma check-list bem estruturada pode conter centenas de itens. A efetividade depende da
        qualidade, atualização e aplicação correta da check-list.""")

    print("✅ Banco de dados populado com sucesso!")
    stats = library.get_statistics()
    print(f"   📚 {stats['total_norms']} normas")
    print(f"   📄 {stats['total_articles']} artigos/seções")
    print(f"   📝 ~{stats['total_words']:,} palavras indexadas")
