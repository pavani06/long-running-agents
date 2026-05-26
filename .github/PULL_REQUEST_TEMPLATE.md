## Resumo

<!-- O que este PR faz e por quê? 1–3 frases. -->

## Mudanças

<!-- Liste os arquivos/módulos alterados e o que mudou em cada um. -->

- 

## Testes

<!-- Como foi testado? Quais suites rodam? Resultados esperados? -->

- [ ] `npm run test:regression:mock` passou
- [ ] Nenhum teste novo quebrou

---

## Crossroad-file impact

<!-- Se este PR NÃO toca nenhum crossroad file, escreva "N/A" e apague o checklist abaixo. -->
<!-- Se TOCA um crossroad file, preencha o checklist. -->
<!-- Crossroad files: src/lib/safe-console.js, src/lib/logger.js, src/lib/redaction.js, src/persistence/supabase-client.js, tests/helpers/supabase-mock.js -->
<!-- Política completa: docs/guides/crossroad-change-policy.md | CODEOWNERS: .github/CODEOWNERS -->

**Arquivo(s) crossroad afetado(s):**

<!-- ex: src/lib/safe-console.js -->

**Tipo de mudança:**

<!-- API change / additive export / internal only -->

**Nota de migração / consumer impact:**

<!-- Se API pública mudou: liste o que mudou e quais importers foram verificados. -->
<!-- Se supabase-client.js ou supabase-mock.js: descreva parity com o Supabase real. -->

**Checklist do revisor:**

- [ ] Migration note presente (se API alterada)
- [ ] Consumer impact documentado (módulos afetados listados)
- [ ] Regression suite verificada
- [ ] Mock parity mantida (se supabase-client/mock alterados)
- [ ] Code-owner approval obtida
