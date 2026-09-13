<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../REVIEW.md). Se o texto for diferente, a fonte em inglês é oficial.

<a id="installer-review"></a>

# Revisão do instalador

Autor: Neil Mitchell  
Criador: Neil Mitchell  
Última modificação por: Neil Mitchell

Revisou o novo aplicativo em relação à lista de verificação de revisão do GStack, incluindo uma revisão de segurança independente somente leitura. Todos os problemas de implementação identificados foram resolvidos no âmbito do trabalho do instalador autorizado:

- Um executável ausente pode impedir a seleção do cliente para recuperação de falhas. A seleção de pasta agora descobre e valida registros de recuperação antes de inspecionar WoW.exe. Um teste de regressão GUI cobre o caso de executável ausente.
- Os downloads ocorreram antes do bloqueio da operação. Uma concessão agora cobre o cache de download por meio de commit; a recuperação pendente é verificada dentro desse arrendamento.
- Temporários graváveis ​​previsíveis podem seguir hardlinks NTFS. Temporários de diário e assembly agora usam nomes GUID com CreateNew. Os arquivos parciais retomados são abertos exclusivamente e sua contagem de links é verificada antes de qualquer truncamento ou gravação. Um teste de regressão de hardlink prova que o arquivo não relacionado permanece inalterado.
- Um diário de restauração violado pode criar um bloqueio em outra raiz antes da validação. Tamanho, localização, raiz, localidade, entradas e caminhos com escopo agora são validados antes de adquirir o bloqueio de restauração. Um teste de regressão prova que nenhum bloqueio estrangeiro foi criado.
- A restauração interrompida não tinha seu próprio estado retomável. RESTORING é registrado em diário antes da mutação e reconhecido em toda a interface do usuário e no caminho de recuperação. Injeção de falhas após cada etapa de restauração.
- As opções de mapa instaladas/restauradas podem permanecer obsoletas na IU. A detecção do cliente é atualizada após cada operação bem-sucedida. O teste GUI instala a seleção do mapa, verifica seu estado retido, restaura e verifica o estado anterior.

A migração GitHub fixa adicionalmente o repositório, a tag de lançamento e o nome do arquivo no catálogo incorporado. Os redirecionamentos são seguidos manualmente para que cada destino HTTPS seja verificado antes de uma solicitação, incluindo credenciais e verificações de porta. O antigo analisador de confirmação HTML do Google Drive foi removido. Testes adicionados cobrem adulteração de URL do catálogo, uma transferência recuperável redirecionada e destinos de redirecionamento rejeitados.

Uma análise independente da migração descobriu que a otimização do Python poderia remover as verificações de publicação escritas como asserções. As verificações de upload, atualização de catálogo e liberação agora geram exceções explícitas. O uploader também resolve cada fonte e exige que ela permaneça diretamente dentro do diretório de carga útil. Os testes de proteção de publicação passam em `python -O` para caminhos de arquivo, tamanhos, hashes e adulteração remota de URL/resumo.

Conjunto de regressão completo mais recente: `reports/tests-20260911-200603/results.json`; Grupos de teste 38 aprovados, incluindo combinações reais de instalação/restauração de dispositivos 108, todos os pontos de interrupção de confirmação/restauração, proteção de caminho/junção/hardlink, bloqueios de processos e arquivos, corrupção/desvio, manipulação de intervalo HTTP, cancelamento, montagem offline e instalação/restauração de GUI usando o executável com versão real.

A análise da IU 1.0.1 cobre texto de suporte mais brilhante, texto de rodapé maior e pintura personalizada de controle desativado. A semântica nativa habilitada permanece em vigor; apenas a aparência desativada é desenhada manualmente. As visualizações iniciais, prontas e ocupadas do Windows foram inspecionadas visualmente. Core.cs, Downloader.cs e todas as cargas úteis do jogo permanecem idênticas em bytes à v1.0.0. Suas evidências de jogo/rede são retidas; o conjunto de regressão Windows é executado novamente para esta atualização. A investigação de viabilidade Wine não passou na construção do formulário e não estabelece suporte de plataforma.

As verificações de publicação e os metadados binários finais são portas separadas. Consulte o lançamento VALIDATION.json para obter o escopo das evidências, incluindo quais verificações foram retidas da linha de base inalterada do jogo.

<a id="installer-110"></a>

## Instalador 1.1.0

A implementação do Wine seguiu um Conselho de três opiniões e duas revisões por pares.
Ele mantém o mecanismo de transação C# e requer um Linux autenticado ao vivo
auxiliar para inspeção de caminho Wine, verificações de processo de host e bloqueio de prefixo cruzado.
O auxiliar rejeita links, invólucros ambíguos, visibilidade restrita do processo e
sistemas de arquivos não suportados. Os mapeamentos de unidade Wine são aceitos somente após
inspeção de alvo. A política do processo requer de forma conservadora todos os WoW
instâncias a serem encerradas. Verificações repetidas reduzem corridas; eles não bloqueiam
programas não relacionados ou eliminar alterações hostis e simultâneas no sistema de arquivos.

A revisão de implementação focada encontrou cobertura de montagem aninhada e liberação de bloqueio
depois de uma raiz renomear lacunas. Ambos foram corrigidos: caminhos gerenciados e seus mais próximos
os ancestrais existentes devem permanecer no sistema de arquivos local do cliente e liberar
usa o caminho nativo e o token salvos sem exigir que a raiz ainda exista.
Os testes nativos correspondentes são aprovados.

As verificações de espaço livre agora consultam o cache Linux real e os sistemas de arquivos do cliente,
em vez da raiz da unidade mapeada de Wine. Testes reais de download e instalação do Wine
com zero espaço livre relatado, rejeite a operação e preserve os arquivos originais.

A validação inclui grupos 38 em Windows e 38 em testes auxiliares nativos Wine, 15,
8 Wine casos de segurança incluindo dois prefixos e perda de auxiliar após uma movimentação, um
nova instalação/reversão anônima de GitHub em Wine e um inicializador de usuário normal
e transação de fixação. O ICO W-and-shield é copiado byte por byte do
favicon do site de lançamento existente. Os snapshots da IU abrangem inicial, pronto e ocupado
estados; a ramificação de pré-requisito Windows foi revisada e o tempo de execução instalado
caminho exercido. Nenhuma máquina Windows sem .NET foi modificada para um teste.
O código final também repete a instalação principal e a reversão exata com o
bytes de carga útil GitHub previamente baixados e refeitos.

<a id="setup-117-review"></a>

## Configuração da revisão 1.1.7

Revisou a comparação atual para escopo de caminho, confiança de origem local, seleção de download, verificações de desvio de preflight/commit, backups de transações e compatibilidade de reversão. Nenhuma descoberta não resolvida. A reutilização local é limitada ao par S raiz/localidade ativa correspondente ao catálogo; os arquivos desativados são movidos pelo diário de backup verificado existente. Ambas as plataformas passaram por grupos de regressão 50 e ativação/desativação/ativação do arquivo de lançamento real com reversão empilhada exata. Nenhuma alteração na carga útil do jogo.
