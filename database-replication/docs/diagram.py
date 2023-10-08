from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Python
from diagrams.generic.compute import Rack
from diagrams.generic.database import SQL
from diagrams.onprem.database import PostgreSQL, Mssql
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Zookeeper


ATTRS = {
    "fontname": "JetBrainsMono Nerd Font Mono",
    "nodesep": "0.90",
    "ranksep": "1.0",
}


with Diagram(
    "Design Architecture",
    show=False,
    direction="LR",
    graph_attr=ATTRS,
    node_attr=ATTRS,
    edge_attr=ATTRS,
):
    upstream_app = Python("Upstream app")
    source_db = PostgreSQL("Source database")
    sink_db = Mssql("Sink database")

    with Cluster("Kafka Connect", graph_attr=ATTRS):
        with Cluster("Debezium CDC Source Connector", graph_attr=ATTRS):
            source_workers = Rack("Producer")

        with Cluster("JDBC Sink Connector", graph_attr=ATTRS):
            consumer_1 = SQL("Consumer Topic 1")
            consumer_2 = SQL("Consumer Topic 2")

    with Cluster("Kafka Ecosystem", graph_attr=ATTRS):
        with Cluster("Kafka Cluster", graph_attr=ATTRS):
            kafka_0 = Kafka("Broker 0")
            kafka_1 = Kafka("Broker 1")
            kafka_2 = Kafka("Broker 2")
            kafka_0 >> kafka_1 >> kafka_0
            kafka_2 >> kafka_1 >> kafka_2
            brokers = [kafka_0, kafka_1, kafka_2]
        zookeeper = Zookeeper("Zookeeper")

    # Upstream app generate data to PostgreSQL
    upstream_app >> Edge(label="generate data") >> source_db

    # PostgreSQL publish to Debezium
    source_db >> Edge(label="produce") >> source_workers

    # DBZ workers produce msg to kafka
    source_workers >> kafka_1
    zookeeper - Edge(label="get broker id", style="dashed") - source_workers

    # JDBC workers consume msg from kafka
    kafka_1 >> consumer_1
    kafka_1 >> consumer_2
    zookeeper - Edge(label="udpate offset", style="dashed") - consumer_1

    # Pull to MSSQL
    consumer_1 >> sink_db
    consumer_2 >> sink_db
