# STEER.md — Canal de Redirecionamento

> Este arquivo é monitorado pelo agente. Escreva aqui para redirecionar o
> agente no meio de uma sessão longa sem precisar reiniciar.
>
> O agente lê este arquivo periodicamente. Se encontrar conteúdo, ele:
> 1. Lê a orientação
> 2. Incorpora imediatamente (prioridade sobre o plano atual)
> 3. Limpa o arquivo (para evitar re-leitura)
>
> **Uso:** `echo "sua orientação aqui" > STEER.md`
>
> **Exemplos:**
> - "Pare de usar PostgreSQL. Migre tudo para SQLite."
> - "Ignore a feature atual. Priorize correção de bug no login."
> - "O layout está muito escuro. Use tons mais claros no tema."
> - "Antes de continuar, adicione testes para o módulo auth."

<!-- Apague esta mensagem placeholder na primeira vez que usar o canal -->
