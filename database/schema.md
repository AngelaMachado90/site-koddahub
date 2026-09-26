# Modelo de dados do Portal KoddaHub

```mermaid
erDiagram
    ORGANIZATIONS ||--o{ ORGANIZATION_MEMBERS : has
    USERS ||--o{ ORGANIZATION_MEMBERS : joins
    USERS ||--o{ USER_IDENTITIES : authenticates
    ORGANIZATIONS ||--o{ ORGANIZATION_PRODUCTS : enables
    PRODUCTS ||--o{ ORGANIZATION_PRODUCTS : includes
    ORGANIZATION_PRODUCTS ||--o{ TICKETS : scopes
    USERS ||--o{ TICKETS : creates
    USERS o|--o{ TICKETS : assigned
    TICKETS ||--o{ TICKET_MESSAGES : contains
    USERS ||--o{ TICKET_MESSAGES : authors
    TICKET_MESSAGES ||--o{ TICKET_ATTACHMENTS : carries
    USERS ||--o{ TICKET_ATTACHMENTS : uploads
    TICKETS ||--o{ TICKET_EVENTS : records
    USERS o|--o{ TICKET_EVENTS : acts
```

`ORGANIZATION_PRODUCTS` é também a fronteira de integridade dos tickets: a FK composta impede que um ticket associe uma organização a um produto não habilitado para ela. O diagrama omite colunas para destacar as relações; as constraints completas estão nas migrations.
