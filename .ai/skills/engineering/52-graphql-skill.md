# GraphQL Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Design e implementação de APIs GraphQL: schema, resolvers, subscriptions.

## Princípios
- Schema-first design
- Resolvers finos (não gordos)
- N+1 prevention (DataLoader)
- Versionamento via deprecation

## Inputs
- Modelo de dados
- Casos de uso
- Queries necessárias

## Outputs
- Schema SDL
- Resolvers
- Types e inputs

## Componentes

```graphql
# Schema
type User {
  id: ID!
  name: String!
  email: String!  @deprecated(reason: "Use contactInfo")
  posts: [Post!]!
}

type Query {
  user(id: ID!): User
  users(limit: Int = 10): [User!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}

type Subscription {
  userCreated: User!
}
```

## Ferramentas

| Ferramenta | Uso |
|---|---|
| Apollo Server | Node.js |
| GraphQL Yoga | Node.js, lightweight |
| Strawberry | Python |
| Ariadne | Python |
| gqlgen | Go |
| Hasura | Postgres-native |

## Invariantes
- Schema versionado
- N+1 queries prevenidos (DataLoader)
- Profundidade máxima de query limitada
- Rate limiting por complexidade
- Persisted queries em produção

## Performance

```python
# DataLoader para N+1
user_loader = DataLoader(async (ids) => {
  return User.findByIds(ids)
})

# Resolver
User.posts = (parent, args, ctx) => {
  return post_loader.load(parent.id)
}
```

## Interfaces
- API Skill
- Performance Skill
- Database Skill
- Security Architect

## Ver Também

- `15-api-skill.md`
- `41-api-versioning-skill.md`
- `14-database-skill.md`
