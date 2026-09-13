<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](README.md)
<!-- LANGUAGES:END -->

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../PLATFORM-FEASIBILITY.md). Se o texto for diferente, a fonte em inglês é oficial.

<a id="lau-setup-platform-feasibility"></a>

# Viabilidade da plataforma Lau Setup

Autor: Neil Mitchell  
Criador: Neil Mitchell  
Última modificação por: Neil Mitchell  
Data de avaliação: 2026-09-11

Atualização: o usuário selecionou apenas Wine. O instalador 1.1.0 agora fornece o testado
Wine 11 / Wine Mono 10.4.1 iniciador descrito no [guia Wine](wine/README.md).
A sonda Wine 8 e as recomendações abaixo são preservadas como avaliação histórica.
A integração de Lutris, Proton e macOS permanece fora do escopo.

Lau Setup 1.0.1 continua sendo um instalador Windows. Linux a Wine é o próximo alvo de compatibilidade recomendado. Esta avaliação não certifica a instalação em Linux ou macOS. Os casos anteriores do 63 Docker/Wine exerciam os dados do jogo, não este instalador.

| Opção | Recomendação | O que isso significa para Lau Setup |
| --- | --- | --- |
| Wine em Linux | Primeiro alvo; viável em princípio, atualmente não verificado | Reutilize o instalador Windows dentro de um prefixo Wine explicitamente selecionado. Prove seu tempo de execução, seleção de pastas, downloads, segurança de arquivos e recuperação antes de publicar suporte. |
| Lutris | Em seguida, após passar Wine direto | Uma pequena receita de integração pode iniciar a configuração no prefixo do jogo existente. Nenhum formato de carga útil separado é necessário. |
| Vapor / Próton | Mais tarde, condicional | Use o prefixo correto do jogo existente. Adicionar configuração como outro jogo não Steam pode proporcionar um ambiente diferente. A usabilidade do Steam Deck precisa de verificações separadas de tela e controlador. |
| CrossOver no macOS | Pista de teste separada e plausível | Corra dentro da garrafa do jogo. Valide no hardware macOS real e nas versões CrossOver suportadas; Os testes Linux não podem estabelecer isso. |
| Wine + DXVK | Configuração opcional do jogo | DXVK traduz Direct3D para o jogo. Isso não resolve os requisitos de segurança de arquivos, fontes ou .NET do instalador. |
| Uísque | Não adotar como nova meta de apoio | Seu projeto upstream não é mais mantido ativamente. |

A classificação acima segue as funções descritas por [Wine Mono](https://github.com/wine-mono/wine-mono), [Lutris](https://lutris.net/about/), [Proton](https://github.com/ValveSoftware/Proton), [DXVK](https://github.com/doitsujin/dxvk), [CrossOver's Mac guia](https://support.codeweavers.com/en_US/crossover-mac-user-guide) e [Uísque](https://github.com/Whisky-App/Whisky). As recomendações são nossa avaliação, não a certificação upstream de Lau Setup. CrossOver pode executar aplicações 32-bit Windows em frascos 64-bit; a perda do suporte nativo do macOS 32-bit por si só não descarta isso.

<a id="bounded-probe-results"></a>

## Resultados de sondagem limitados

A investigação local usou Wine 8.0 (Debian 8.0~repack-4), um prefixo win32 isolado e Xvfb. Este tempo de execução mais antigo disponível localmente não é um teste das versões Wine atuais. Nenhum cliente de jogo pessoal foi montado ou modificado.

1. A imagem de teste de jogo herdada desativou o mscoree. Habilitando-o exposto que Wine Mono estava faltando. Este foi um problema do ambiente de teste.
2. Instalei o oficial Wine Mono 7.4.0 MSI no prefixo descartável após verificação SHA-256 `6413ff328ebbf7ec7689c648feb3546d8102ded865079d1fbf0331b14b3ab0ec`, fixado por [Wine 8.0fonte](https://raw.githubusercontent.com/wine-mirror/wine/wine-8.0/dlls/appwiz.cpl/addons.c).
3. Um chicote de diagnóstico inicializado WinForms e carregou o catálogo incorporado e falhou ao construir o formulário com `System.ArgumentException: The requested FontFamily could not be found [GDI+ status: FontFamilyNotFound]`. Copiar as fontes Liberation disponíveis para esse prefixo não resolveu o problema. Nenhuma captura de tela ou instalação do instalador foi bem-sucedida.
4. As evidências locais são retidas sob `reports/wine-feasibility/`. O contêiner de análise está parado. O equipamento de diagnóstico não está incluído no instalador distribuído ou no pacote de origem pública.

Isso identifica o trabalho de provisionamento de tempo de execução/fonte, e não prova que Wine é impossível. Nenhuma transação de instalação/restauração foi tentada em Wine neste probe.

<a id="acceptance-work-before-wine-support"></a>

## Trabalho de aceitação antes do suporte Wine

1. Estabeleça uma combinação Wine/tempo de execução/fonte atual reproduzível em um desktop Linux. Mostrar estados inicial, pronto, download, recuperação e erro em escalas de exibição comuns; verifique o acesso ao teclado e a seleção de pastas.
2. Verifique o mapeamento exato da pasta host e o tratamento de maiúsculas e minúsculas em um sistema de arquivos com distinção entre maiúsculas e minúsculas, incluindo nomes duplicados que diferem apenas por maiúsculas e minúsculas. Preservar patches não relacionados e configurações pessoais.
3. Prove o comportamento de link, bloqueio exclusivo, espaço livre, diário e substituição atômica. O instalador atualmente chama APIs de informações de arquivo Windows; sua semântica deve ser testada em Wine em vez de assumida.
4. Prove a proteção do jogo em execução entre os prefixos. O código atual enumera processos Windows e compara diretórios executáveis. A visibilidade do prefixo Wine pode deixar outro prefixo executando o mesmo cliente sem ser detectado. Resolva isso antes de oferecer suporte de instalação segura; um teste bem-sucedido do mesmo prefixo por si só é insuficiente.
5. Execute a matriz de instalação/restauração e recuperação interrompida do equipamento e, em seguida, um download/instalação/reversão anônimo limpo do GitHub usando ativos de lançamento exatos. Teste TLS, redirecionamentos, retomada, cancelamento e recuperação offline.
6. Em seguida, faça uma verificação no jogo no mesmo ambiente compatível. Só então publique as instruções Wine e uma integração Lutris. Mantenha o Proton e o macOS explicitamente não verificados até que suas próprias verificações sejam aprovadas.

Mantenha um conjunto de ativos de jogo imutáveis ​​nas versões GitHub. Não adicione clientes completos, UI pessoal ou cópias de cada carga útil ao repositório Git para ativar outro inicializador. Se Wine não puder satisfazer as verificações de segurança de maneira confiável, avalie um instalador nativo Linux com base no mesmo manifesto e regras de transação como uma implementação separada.
