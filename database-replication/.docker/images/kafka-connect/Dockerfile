FROM confluentinc/cp-server-connect:7.1.1

RUN echo "INFO: Installing Connectors"
RUN confluent-hub install --no-prompt debezium/debezium-connector-postgresql:2.2.1
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:10.7.4
RUN echo "INFO: Launching Kafka Connect workers"

CMD [ "/etc/confluent/docker/run" ]
