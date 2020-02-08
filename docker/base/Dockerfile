FROM oraclelinux:8-slim

ARG JAVA_VERSION=8.0.232-open
ARG SCALA_VERSION=2.12.10
ARG SBT_VERSION=1.3.7
ARG SPARK_VERSION=2.4.4
ARG HADOOP_VERSION=2.7

ENV DAEMON_RUN=true
ENV PYTHONHASHSEED=1
ENV SDKMAN_DIR=/usr/local/sdkman
ENV JAVA_HOME=${SDKMAN_DIR}/candidates/java/current/
ENV SCALA_HOME=${SDKMAN_DIR}/candidates/scala/current/
ENV SBT_HOME=${SDKMAN_DIR}/candidates/sbt/current/
ENV SPARK_HOME=/opt/spark

RUN touch /etc/dnf/dnf.conf && microdnf update -y
RUN microdnf install bash curl ca-certificates unzip zip tar gzip bzip2 which findutils python3 python3-pip -y && microdnf clean all -y
RUN curl -s "https://get.sdkman.io" | bash
RUN set -x \
    && echo "sdkman_auto_answer=true" > $SDKMAN_DIR/etc/config \
    && echo "sdkman_auto_selfupdate=false" >> $SDKMAN_DIR/etc/config \
    && echo "sdkman_insecure_ssl=false" >> $SDKMAN_DIR/etc/config
RUN bash -c "source $SDKMAN_DIR/bin/sdkman-init.sh && \
    sdk update && sdk upgrade && sdk selfupdate && \
    sdk install java ${JAVA_VERSION} && sdk default java ${JAVA_VERSION} && \
    sdk install scala ${SCALA_VERSION} && sdk default scala ${SCALA_VERSION} && \
    sdk install sbt ${SBT_VERSION} && sdk default sbt ${SBT_VERSION} && \
    sdk flush archives && sdk flush temp && sdk flush broadcast"
RUN pip3 --no-cache-dir install matplotlib pandas simpy numpy scipy
RUN curl -o /tmp/spark.tgz https://www-us.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && tar -xvzf /tmp/spark.tgz --one-top-level=spark --strip-components 1 -C /opt/ && rm -f /tmp/spark.tgz
RUN alternatives --set python /usr/bin/python3

WORKDIR ${SPARK_HOME}