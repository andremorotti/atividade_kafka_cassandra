# E-commerce Sales Simulation with Kafka, PySpark and Cassandra / Simulação de Vendas de E-commerce com Kafka, PySpark e Cassandra

## Steps / Etapas

1. **Setting up Apache Kafka:** Installing and configuring the Kafka environment in KRaft mode and creating a topic for sales messages.  
   **Configuração do Apache Kafka:** Instalação e configuração do ambiente Kafka no modo KRaft e criação de um tópico para as mensagens de vendas.

2. **Creating a Python Message Producer:** Developing a producer that sends simulated sales data messages to Kafka.  
   **Criação de um Produtor de Mensagens em Python:** Desenvolvimento de um produtor que envia mensagens de dados de vendas simulados para o Kafka.

3. **Creating a Message Consumer in PySpark:** Developing a PySpark consumer that reads messages from Kafka, processes the data, and displays the total sales grouped by product.  
   **Criação de um Consumidor de Mensagens em PySpark:** Desenvolvimento de um consumidor em PySpark que lê mensagens do Kafka, processa os dados e exibe o valor total das vendas agrupado por produto.

4. **Storing Aggregated Data in Cassandra:** Saving the aggregated sales data by product into a Cassandra table for persistent storage and querying.  
   **Armazenamento dos Dados Agregados no Cassandra:** Salvando os dados agregados de vendas por produto em uma tabela Cassandra para armazenamento persistente e consultas.
   
## Technologies Used / Tecnologias Utilizadas

- Python: Version 3.x (recommended) / Versão 3.x (recomendado)
- PySpark: Version 3.5.5
- Apache Kafka: Version 4.0.0 (KRaft mode)
- kafka-python: For the Python producer / Para o produtor Python
- Faker: For simulated sales data generation / Para geração de dados de vendas simulados
- Apache Cassandra: Version 4.x / Para armazenamento de dados agregados

## Prerequisites / Pré-requisitos

- **Java Development Kit (JDK):** Kafka is written in Java and requires the JDK installed. / O Kafka é escrito em Java e requer o JDK instalado.
- **Apache Kafka:** Necessary for the message broker. / Necessário para o broker de mensagens.
- **Python and Pip:** Necessary to run the producer and consumer scripts. / Necessários para executar os scripts do produtor e do consumidor.
- **PySpark:** Necessary for processing the data stream from Kafka. / Necessário para o processamento do fluxo de dados do Kafka.
- **Apache Cassandra:** Necessary for storing aggregated data. / Necessário para armazenar os dados agregados.

## Installation and Configuration / Instalação e Configuração

### 1. Setting up Apache Kafka (KRaft Mode) with Environment Variables / Configuração do Apache Kafka (Modo KRaft) com Variáveis de Ambiente

These instructions assume a Linux/macOS operating system. Commands may vary on other systems.

Estas instruções assumem um sistema operacional Linux/macOS. Os comandos podem variar em outros sistemas.

1.  **Download Apache Kafka:**
    ```bash
    mkdir kafka
    cd kafka/
    wget [https://downloads.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz](https://downloads.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz)
    tar -xzf kafka_2.13-4.0.0.tgz
    ```

2.  **Configure Environment Variables:**
    Add the following lines to your shell configuration file (e.g., `~/.bashrc` or `~/.zshrc`), replacing `/opt/kafka` with the path where you installed Kafka:
    Adicione as seguintes linhas ao arquivo de configuração do seu shell (por exemplo, `~/.bashrc` ou `~/.zshrc`), substituindo `/opt/kafka` pelo caminho onde você instalou o Kafka:
    ```bash
    export KAFKA_HOME="/opt/kafka"
    export PATH="$PATH:$KAFKA_HOME/bin"
    ```
    After editing the file, run `source ~/.bashrc` or `source ~/.zshrc` to apply the changes.
    Após editar o arquivo, execute `source ~/.bashrc` ou `source ~/.zshrc` para aplicar as alterações.

3.  **Generate Cluster ID:**
    ```bash
    KAFKA_CLUSTER_ID="$(kafka-storage.sh random-uuid)"
    echo "Kafka Cluster ID: $KAFKA_CLUSTER_ID" # Optional: to view the generated ID / Opcional: para visualizar o ID gerado
    ```

4.  **Format Broker Storage:**
    ```bash
    kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c $KAFKA_HOME/config/server.properties
    ```
    **Warning:** This command formats the Kafka data directory. If you have important data, make a backup first.
    **Atenção:** Este comando formata o diretório de dados do Kafka. Se você já tiver dados importantes, faça um backup antes.

5.  **Start the Kafka Server:**
    ```bash
    kafka-server-start.sh $KAFKA_HOME/config/server.properties
    ```
    Keep this terminal window open. / Mantenha esta janela do terminal aberta.

6.  **Create the Kafka Topic:** Open a new terminal window:
    ```bash
    kafka-topics.sh --create --topic vendas-ecommerce --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    ```
### 2. Setting up Cassandra / Configuração do Cassandra

1. **Download and Install Apache Cassandra:**  
   Follow instructions at [https://cassandra.apache.org/_/quickstart.html](https://cassandra.apache.org/_/quickstart.html).

2. **Start Cassandra Server:**  
   ```bash
   cassandra -f
   ```

3. **Connect to Cassandra Shell:**  
   ```bash
   cqlsh
   ```

4. **Create Keyspace and Table:**  
   ```sql
   CREATE KEYSPACE atividade_cassandra WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

   CREATE TABLE atividade_cassandra.vendas_por_produto (
       nome_produto text PRIMARY KEY,
       valor_total double
   );
   ```
### 3. Project Environment Setup / Configuração do Ambiente do Projeto

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/andremorotti/atividade_kafka.git
    cd your_repository
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(On Windows systems, use `venv\Scripts\activate`)*
    *(Em sistemas Windows, use `venv\Scripts\activate`)*

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 4. Running the Scripts / Execução dos Scripts

1.  **Run the Message Producer:** Open a new terminal window, navigate to your project directory, and run the Python producer script:
    **Execute o Produtor de Mensagens:** Abra uma nova janela do terminal, navegue até o diretório do seu projeto e execute o script do produtor Python:
    ```bash
    python producer.py
    ```

2.  **Run the Consumer with PySpark:** Open a new terminal window, navigate to your project directory, and run the PySpark consumer script, including the Kafka connector:
    **Execute o Consumidor com PySpark:** Abra uma nova janela do terminal, navegue até o diretório do seu projeto e execute o script do consumidor PySpark, incluindo o conector Kafka:
    ```bash
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5,com.datastax.spark:spark-cassandra-connector_2.12:3.5.0 consumer.py
    ```
    *(Ensure the Spark version matches yours)*
    *(Certifique-se de que a versão do Spark corresponda à sua)*
    
### 5. Storing Aggregated Results in Cassandra / Armazenando os Resultados Agregados no Cassandra

After processing the data in PySpark, the script inserts the aggregated total sales by product into the Cassandra table `vendas_por_produto` under the keyspace `atividade_cassandra`.

Após o processamento dos dados no PySpark, o script insere o total agregado de vendas por produto na tabela `vendas_por_produto` dentro do keyspace `atividade_cassandra`.

### 6. Querying Cassandra / Consultando o Cassandra

Use `cqlsh` to query the stored aggregated results:

```sql
SELECT * FROM atividade_cassandra.vendas_por_produto;
```

### 7. Stopping the Processes / Interrompendo os Processos

To stop any Kafka service (Server, Producer, or Consumer), press `Ctrl + C` in the corresponding terminal window.

Para interromper qualquer serviço do Kafka (Servidor, Produtor ou Consumidor), pressione `Ctrl + C` na janela do terminal correspondente.
