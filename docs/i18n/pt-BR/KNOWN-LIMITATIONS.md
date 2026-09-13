<!-- LANGUAGES:START -->
[English](../../../README.md) · [Deutsch](../de/README.md) · [Español (España)](../es-ES/README.md) · [Español (México)](../es-MX/README.md) · [Français](../fr/README.md) · [한국어](../ko/README.md) · [Русский](../ru/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [Português (Brasil)](README.md)
<!-- LANGUAGES:END -->

<!-- ZIP-ONLY-120-NOTICE -->
> **Setup 1.3.0** — Um único ZIP agora contém o instalador do Windows e o iniciador para Linux/Wine. A interface segue automaticamente o idioma do sistema operacional entre dez opções; a escolha manual é salva. A versão 3.0.8 e os arquivos do jogo não mudam. Não há alterações de DBC.
>
> A atualização completa dos guias continua pendente devido a um HTTP 429 do Google. O texto abaixo pode estar desatualizado; consulte a fonte atual em inglês e as notas da versão 1.3.0. [English](../../../KNOWN-LIMITATIONS.md) · [1.3.0](https://github.com/CRSD-Lau/Lau-Setup/releases/tag/v1.3.0)
>
> **Download atual:** [LauSetup.zip](https://github.com/CRSD-Lau/Lau-Setup/releases/latest/download/LauSetup.zip) para Windows e Linux/Wine. Extraia a pasta `LauSetup/` com cinco arquivos: no Windows, abra `LauSetup.exe`; no Linux/Wine, execute `LauSetup.sh`. As instruções antigas abaixo sobre EXE ou ZIP Wine separados não se aplicam à versão 1.3.0.
>
> **1.3.0:** Os arquivos extras de melhoria reconhecidos são salvos em backup e a instalação continua. A restauração os devolve. Não é preciso movê-los manualmente.

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

> Tradução automática. [Fonte em inglês](../../../KNOWN-LIMITATIONS.md). Se o texto for diferente, a fonte em inglês é oficial.

<a id="known-limitations-and-assumptions"></a>

# Limitações e suposições conhecidas



[Voltar para Lau Setup](README.md) · [Recomendações e solicitações de recursos](https://github.com/CRSD-Lau/Lau-Setup/discussions/1) · [Histórico de alterações do DBC](DBC-CHANGELOG.md)

Leia isto antes de propor um recurso. Lau Setup instala uma atualização visual do lado do cliente para **WoW 3.3.5a build 12340**. Não é uma estrutura de modificação de servidor. Os limites abaixo descrevem o projeto atual; fora do âmbito não significa necessariamente tecnicamente impossível.

<a id="what-we-can-and-cannot-change"></a>

## O que podemos e não podemos mudar

| Solicitação | Limite atual |
| --- | --- |
| Melhorar indicadores de solo, texturas, modelos ou tabelas de clientes localizadas suportadas | Dentro do escopo, sujeito a dependências de arquivo e testes. Uma melhoria visual não deve ser descrita como uma mudança nos danos ou na mecânica do servidor. |
| Melhorar instalação, backups, acessibilidade ou documentação | Dentro do escopo. Preserve arquivos não relacionados e verifique a instalação e recuperação. |
| Alterar dano Warmane, detecção de acerto, duração da habilidade, direcionamento ou scripts de encontro | Fora do nosso controle. Warmane executa seu próprio código de servidor; este projeto não tem acesso para alterar ou implantar esse código. Um MPQ ou addon não pode fazer com que o servidor adote uma mecânica diferente. |
| Adicionar código C++ personalizado ao núcleo do Warmane | Não é algo que esta versão possa oferecer. As alterações em um servidor de teste controlado separadamente não alteram Warmane. |
| Injete uma DLL, conecte o cliente ou adicione um novo comportamento nativo do mecanismo | Fora do fluxo de trabalho de patch/complemento compatível. Isso requer uma investigação separada de engenharia e compatibilidade, não apenas uma edição do DBC. Nenhuma estrutura de injeção de DLL ou suporte geral de gancho de cliente é fornecida. |
| Desbloqueie ações Lua protegidas ou APIs de jogos ausentes | Não é um recurso compatível. Addon editável Lua e ações de cliente protegidas são coisas diferentes. Reescrever Lua por si só não concede permissões nem cria uma API que o cliente não expõe. Relate a ação/API exata antes de assumir que existe uma solução alternativa. |
| Forneça um cliente completo, outro pacote de idiomas ou uma base de modelo HD | Não incluído. Traga um cliente compatível existente com os arquivos de idioma, fontes e configuração de modelo necessários. |

O `WoW.exe` compatível fornecido pela configuração tem uma função específica no renderizador de carregamento aprovado, capacidade de arquivo e suporte para endereços grandes. Sua inclusão **não** é uma promessa de modificações arbitrárias de executáveis ​​ou DLL. Da mesma forma, nem todo arquivo Lua é protegido ou não pode ser editado: alterações comuns de complementos e UI podem ser viáveis ​​dentro do comportamento suportado pelo cliente.

<a id="indicators-are-visual-guidance"></a>

## Indicadores são orientações visuais

- **Warmane é a referência de tempo de execução para relatórios Warmane.** AzerothCore e clientes isolados ajudam a verificar a integridade e o comportamento dos arquivos nesses ambientes. Eles não podem provar a detecção de acertos personalizados, o tempo ou o comportamento de encontro do Warmane.
- **Uma borda desenhada não é um limite seguro garantido.** As respirações suportadas e o Slime Spray usam cones totais 90° seguindo o feedback do testador. O fogo de meteoro Halion usa a ampliação test-v2 aceita. Estes são avisos visuais baseados em observações, não em medições da fonte do servidor Warmane.
- **O terreno pode cortar indicadores planos.** Uma malha de terreno plano pode cruzar encostas, degraus e superfícies irregulares. Ampliá-lo ou elevá-lo não garante a projeção do terreno em todos os lugares.
- **A vida útil do efeito precisa de evidências de encontro.** O feedback da perseguição/fantasma incluiu efeitos que desaparecem após um ou dois segundos. Alterar uma textura, forma ou animação em loop por si só não prova que o cliente manterá a instância do efeito ativa durante toda a busca. Uma correção de tempo precisa de filmagens e evidências de eventos para essa habilidade específica; não trate uma maquete ou construção experimental como uma correção confirmada.
- **Os modelos são ilustrativos.** As animações do site/chat demonstram a aparência. Eles não são gravações ou prova de renderização, duração ou cobertura do jogo.

For boundary or timing reports, include the encounter, ability, difficulty, client edition, `/pyversion`, and a clip showing the lead-up and damage or effect ending. As capturas de tela são úteis, mas os efeitos de perspectiva e sobreposição limitam as medições exatas do raio.

<a id="dbc-and-patch-compatibility"></a>

## DBC e compatibilidade de patches

As tabelas DBC são dados conectados, não switches independentes. Adicionar um visual pode exigir referências de feitiço, visual, kit, efeito e modelo correspondentes. A substituição de uma tabela completa também pode substituir seu texto localizado e entrar em conflito com outro patch que forneça a mesma tabela.

A dependência da localização foi um problema real durante o desenvolvimento deste projeto. Andre e Lau trabalharam juntos. The [historical DBC audit](DBC-CHANGELOG.md) separates the reported development timeline from retained archive evidence: Andre's baseline omitted `Spell.dbc`, not every DBC. Não presuma que copiar uma tabela em inglês para outra localidade seja seguro.

- Use a edição que corresponde à configuração atual do HD/modelo original. Novos visuais de feitiços exigem dependências de HD compatíveis; a detecção não certifica todos os pacotes de modelos de terceiros.
- Se você remover ou desabilitar os patches do modelo HD após a instalação, execute novamente a configuração mais recente para a configuração resultante. Uma edição HD instalada não se converte dinamicamente. Ativos incompatíveis podem produzir imagens ausentes ou incorretas e exigir investigação de falhas; nem uma falha nem um comportamento livre de falhas são garantidos.
- As veiculações de localidade raiz e ativa têm funções distintas. Em particular, os dois arquivos S são diferentes. Siga o [guia de posicionamento](docs/TECHNICAL.md#file-placement), não uma instrução genérica para duplicar cada MPQ.
- Patches não relacionados são preservados, mas a preservação não é uma garantia de compatibilidade. Outro arquivo que substitua os mesmos dados pode alterar o resultado.
- A interface do instalador segue automaticamente o idioma do sistema entre dez opções; a escolha manual é salva. O conteúdo do jogo continua a oferecer suporte a nove localidades. Alterar apenas `Config.wtf` não instala arquivos ou fontes de outro idioma.

<a id="installer-and-recovery-assumptions"></a>

## Suposições do instalador e recuperação

Feche WoW totalmente antes da instalação ou restauração. Use exatamente a pasta do cliente pretendida e mantenha `LauSetupBackups` intacto.

A instalação compara hashes de arquivos reais com seu **catálogo incorporado**. Uma alteração de um byte pode ser detectada mesmo quando o tamanho e o carimbo de data/hora correspondem, mas um instalador antigo ainda conhece apenas seu catálogo antigo. Baixe o instalador mais recente ao atualizar. A instalação não monitora continuamente um cliente depois que ele sai ou reconcilia automaticamente alterações manuais de patch posteriores.

Desativar novos visuais de feitiço preserva os arquivos S com escopo como `.mpq.disabled`. A reativação usa bytes desativados correspondentes quando disponíveis e move a cópia simples desativada para o backup da transação verificada. Cópias mais antigas com sufixo hash são retidas. Consulte a [implementação de recuperação atual](docs/TECHNICAL.md#setup-117-re-enable-cleanup).

A restauração depende dos backups e registros de recuperação. Ele para quando alterações posteriores tornam a restauração automática insegura. Não pode prometer a recuperação de arquivos cujo único backup foi excluído. A remoção do Patch-Y por si só não é uma reversão completa do executável e de outros patches instalados pela instalação. Use **Restaurar instalação anterior** para a transação gerenciada.

<a id="platform-and-validation-limits"></a>

## Limites de plataforma e validação

O destino Windows documentado é Windows 10/11 com .NET Framework 4.8. A configuração Linux testada usa Wine 11.0, Wine Mono 10.4.1, um prefixo 64-bit existente e Python 3.9+. Os instaladores de tempo de execução não estão incluídos. Siga os [pré-requisitos Wine](wine/README.md); use armazenamento local Linux. Pastas vinculadas, compartilhamentos de rede e unidades montadas em Windows estão fora da configuração de caminho Wine compatível.

Lutris, Proton, integração específica do Steam Deck e macOS não são alvos de integração suportados nesta versão. Isto não afirma que qualquer outro ambiente seja impossível; isso significa que não estabelecemos suporte para isso. Os pacotes para Windows não possuem assinatura digital.

Construções, verificações de hash, testes de regressão do instalador, testes Wine e testes no jogo respondem a diferentes perguntas. A aprovação em um não substitui os outros. As verificações visuais são amostradas, não certificação de cada zona, encontro, escala de exibição, distribuição Linux ou modificação de cliente de terceiros. Consulte o relatório de validação de cada versão para saber o que realmente foi verificado.

<a id="before-requesting-a-feature"></a>

## Antes de solicitar um recurso

Descreva o problema visível ao jogador, sua configuração e as evidências. Propostas dentro do escopo apoiado são bem-vindas em [Ideias](https://github.com/CRSD-Lau/Lau-Setup/discussions/categories/ideas); defeitos reproduzíveis pertencem a [Problemas](https://github.com/CRSD-Lau/Lau-Setup/issues/new/choose).

Para propostas de DLL, código nativo, ação protegida ou dependentes de servidor, identifique a dependência explicitamente. Necessitam de trabalho de viabilidade e de controlo adequado do sistema afectado antes que a implementação possa ser prometida. Por favor, não os arquive como simples opções DBC ausentes.
