# 🔄 Orquestrador em Grafo (DAG), Checkpoints e Rollback Transacional

O **AI-Brain-Framework** inclui um motor avançado de orquestração baseado em **Grafos Acíclicos Dirigidos (DAG)** com **Checkpoints de Estado**, **Rollback Transacional** e **Padrão Saga (Compensações)** desenvolvido em **Python 3.8+ puro (zero dependências externas)**.

Inspirado nos maiores frameworks de orquestração do mundo (*LangGraph, Temporal, Prefect, Microsoft Agent Framework e Smolagents*), ele permite construir fluxos de agentes e pipelines corporativos com resiliência de nível industrial.

---

## 🏛️ Principais Capacidades

| Recurso | Descrição |
| :--- | :--- |
| **Topologia em Grafo (DAG)** | Resolução de dependências via **Algoritmo de Kahn**, com detecção matemática de ciclos (`CyclicDependencyError`). |
| **Bifurcação Condicional** | Arestas dinâmicas (`add_conditional_edge`) que decidem a próxima rota de acordo com a saída do nó. |
| **Time-Travel Checkpoints** | `context.checkpoint("savepoint_1")` e `context.rollback("savepoint_1")` com snapshots profundos do estado. |
| **Padrão Saga (Compensações)** | Funções de limpeza (`compensate`) disparadas na ordem inversa caso ocorra erro em nós subsequentes. |
| **Execução Paralela (Fan-Out / Fan-In)** | Processamento concorrente de nós independentes via `ThreadPoolExecutor` nativo. |
| **Human-in-the-Loop (HITL)** | Pausa da execução antes de nós críticos (`requires_human_approval=True`) até confirmação explícita. |
| **Retries com Backoff** | Tentativas automáticas com tempo de espera por nó para tolerância a falhas transitórias. |

---

## 🚀 Como Usar na Prática

### 1. Criando um Grafo com Bifurcação Condicional

```python
from framework import Context, create_default_orchestrator, WorkflowDAG

orch = create_default_orchestrator()

# Cria o Grafo
dag = WorkflowDAG(name="agent_security_workflow")

# Adiciona nós
dag.add_node("prompt_shield", skill_name="prompt_shield")
dag.add_node("brain_routing", skill_name="brain", depends_on=["prompt_shield"])
dag.add_node("security_audit", skill_name="security", depends_on=["brain_routing"])
dag.add_node("quarantine_node", action=lambda ctx: ctx.log("Quarantined!"), depends_on=["prompt_shield"])

# Roteamento condicional a partir do prompt_shield
def route_shield(result, ctx):
    return "safe" if result.output.get("is_safe") else "unsafe"

dag.add_conditional_edge(
    source_node="prompt_shield",
    router=route_shield,
    routes={"safe": "brain_routing", "unsafe": "quarantine_node"}
)

ctx = Context()
ctx.set("prompt", "Como construir um sistema web?")
ctx.set("action", "enforce")

# Executa o Grafo
dag_result = orch.run_dag(dag, ctx)

print(dag_result.status.value)        # success
print(dag_result.executed_nodes)       # ['prompt_shield', 'brain_routing', 'security_audit']
print(dag_result.skipped_nodes)        # ['quarantine_node']
```

---

### 2. Time-Travel Checkpoints e Rollback Manual

```python
from framework import Context

ctx = Context()
ctx.set("user_id", 100)
ctx.set("balance", 500.0)

# 1. Salva Checkpoint
cp1 = ctx.checkpoint("saldo_inicial")

# 2. Modifica estado
ctx.set("balance", 200.0)
ctx.set("status", "pending_transaction")

# 3. Rollback para o estado original
ctx.rollback("saldo_inicial")

print(ctx.get("balance")) # 500.0 (restaurado com sucesso!)
print(ctx.has("status"))  # False (modificações desfeitas)
```

---

### 3. Padrão Saga com Compensação Automática em Caso de Falha

```python
from framework import Context, Orchestrator, WorkflowDAG, SkillResult, SkillStatus

dag = WorkflowDAG(name="saga_order_processing")

# Ações de compensação
def undo_reserve_inventory(ctx):
    ctx.set("inventory_reserved", False)

def undo_charge_card(ctx):
    ctx.set("card_charged", False)

# 1. Reserva estoque
dag.add_node(
    "reserve_inventory",
    action=lambda ctx: ctx.set("inventory_reserved", True) or SkillResult(status=SkillStatus.SUCCESS),
    compensate=undo_reserve_inventory
)

# 2. Cobra cartão
dag.add_node(
    "charge_card",
    action=lambda ctx: ctx.set("card_charged", True) or SkillResult(status=SkillStatus.SUCCESS),
    depends_on=["reserve_inventory"],
    compensate=undo_charge_card
)

# 3. Emissão fiscal (falha intencional)
dag.add_node(
    "issue_invoice",
    action=lambda ctx: SkillResult(status=SkillStatus.ERROR, error="SEFAZ offline"),
    depends_on=["charge_card"]
)

orch = Orchestrator()
ctx = Context()

# Executa com auto_rollback_on_error=True
result = orch.run_dag(dag, ctx, auto_rollback_on_error=True)

print(result.status.value)           # error
print(result.failed_node)             # 'issue_invoice'
print(result.rollback_performed)      # True
print(result.compensated_nodes)       # ['charge_card', 'reserve_inventory'] (compensados na ordem reversa!)
```

---

### 4. Execução Paralela em Camadas (Fan-Out / Fan-In)

```python
dag = WorkflowDAG(name="parallel_analysis")

# Nós independentes (Camada 1 - Paralela)
dag.add_node("scan_security", skill_name="security")
dag.add_node("scan_tokens", skill_name="token_economy")

# Nó convergente (Camada 2 - Fan-In)
dag.add_node(
    "consolidated_report",
    action=lambda ctx: SkillResult(status=SkillStatus.SUCCESS, output={"report": "OK"}),
    depends_on=["scan_security", "scan_tokens"]
)

# Executa com parallel=True
result = orch.run_dag(dag, ctx, parallel=True, max_workers=2)
```

---

### 5. Human-in-the-Loop (HITL)

```python
dag = WorkflowDAG(name="hitl_deployment")

dag.add_node("run_tests", action=lambda ctx: SkillResult(status=SkillStatus.SUCCESS))
dag.add_node(
    "deploy_production",
    action=lambda ctx: SkillResult(status=SkillStatus.SUCCESS, output={"deployed": True}),
    depends_on=["run_tests"],
    requires_human_approval=True
)

ctx = Context()

# 1ª Tentativa: Sem aprovação humana
res1 = orch.run_dag(dag, ctx)
print(res1.skipped_nodes) # ['deploy_production'] (pausado aguardando aprovação)

# 2ª Tentativa: Humano aprova
ctx.set("human_approved", True)
res2 = orch.run_dag(dag, ctx)
print(res2.executed_nodes) # ['run_tests', 'deploy_production'] (executado com sucesso!)
```
