# Arch

The architecture can be detailed in general terms on two levels: web and database. The mechanics are abstracted to a general level, avoiding in-depth details that confuse rather than aggregate, presenting a behavioral vision on a "macro" scale following the flow of data without focusing on the "micro", such as each action of each function. Below is the flow of information on the Web, followed by the structuring and architecture of the Database (For more details on the Database go to [https://dbdocs.io/lucasgoncsilva04/SWARDEN](https://dbdocs.io/lucasgoncsilva04/SWARDEN)):

## Web

```mermaid
flowchart LR


User((User))

subgraph CLOUD
    subgraph RENDER
        LB(Load Balancer):::Arch
        Dispatcher[Req. Dispatcher]:::Arch
        Template{{Template}}:::Arch
        View{View}:::Arch
        Model{{Model}}:::Arch
    end

    subgraph SUPABASE
        Database[(Database)]
    end
end


Template ~~~ Model

User --> LB --> Dispatcher --> View --> Model

Model -->|Insert / Update| Database
Model -->|Select| Database

Database --> Model --> View --> Template --> Dispatcher --> LB --> User


style CLOUD fill:#1111,color:#0f0,stroke:#ccc;
style RENDER fill:#1111,color:#0f0,stroke:#ccc;
style SUPABASE fill:#1111,color:#0f0,stroke:#ccc;
style User fill:#fff,color:#080,stroke:#080;
style Database fill:#dfd,color:#080,stroke:#080;

classDef Arch fill:#080,color:#efe,stroke:#efe;

linkStyle 1,2,3,4,5,6 stroke:#0fa,color:#efe
linkStyle 7,8,9,10,11,12 stroke:#aaa,color:#efe
```

## DB

![Database Arch](./assets/db.svg)
