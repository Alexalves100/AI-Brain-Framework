# API Testing Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Testes automatizados de APIs: contract, integration, performance.

## Princípios
- Contract-first testing
- Isolamento entre testes
- Dados reproduzíveis
- CI obrigatório

## Inputs
- API spec (OpenAPI, GraphQL SDL)
- Cenários de teste
- Dados de teste

## Outputs
- Testes passando/falhando
- Relatórios de cobertura
- Métricas de performance

## Tipos de Teste

| Tipo | Quando | Ferramenta |
|---|---|---|
| Contract | Spec mudou | Pact, Dredd |
| Integration | Toda API | Supertest, pytest |
| E2E | Fluxos críticos | Playwright, Cypress |
| Performance | Antes de release | k6, Locust |
| Security | Antes de release | OWASP ZAP |
| Smoke | Pós-deploy | curl, httpie |

## Ferramentas

| Ferramenta | Linguagem |
|---|---|
| Postman/Newman | Multi |
| Jest + Supertest | Node.js |
| pytest + requests | Python |
| JUnit + RestAssured | Java |
| Go testing + httptest | Go |

## Invariantes
- Testes rodam em CI
- Cobertura > 80%
- Testes determinísticos
- Sem dependência entre testes
- Dados de teste isolados

## Workflow

```
1. Spec da API (OpenAPI/SDL)
2. Gerar testes base
3. Adicionar cenários
4. Mock de dependências
5. Rodar localmente
6. CI valida
7. Relatórios de cobertura
```

## Interfaces
- Testing Architect
- API Skill
- CI/CD
- Quality Architect

## Ver Também

- `19-testing-skill.md`
- `15-api-skill.md`
- `11-quality-skill.md`
