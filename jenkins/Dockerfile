FROM jenkins/jenkins:lts
USER root

ENV JENKINS_USER admin
ENV JENKINS_PASS Raymond

#id_rsa.pub file will be saved at /root/.ssh/
RUN ssh-keygen -f /root/.ssh/id_rsa -t rsa -N ''  

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive
# Install necessary packages and Docker CLI
RUN apt-get update && apt-get install -y lsb-release apt-utils iptables iproute2 python3 python3-pip python3-venv curl
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc https://download.docker.com/linux/debian/gpg && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.asc] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli && apt-get clean && ln -s /usr/bin/python3 /usr/bin/python && rm -rf /var/lib/apt/lists/*
# Install docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

# allows to skip Jenkins setup wizard
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

# Jenkins runs all grovy files from init.groovy.d dir
# use this for creating default admin user
COPY default-user.groovy /usr/share/jenkins/ref/init.groovy.d/

VOLUME /var/jenkins_home

USER jenkins

RUN jenkins-plugin-cli --plugins "blueocean docker-workflow warnings-ng dependency-check-jenkins-plugin pipeline-stage-view sonar maven-plugin maven-invoker-plugin"

ARG MAVEN_VERSION=3.6.3
ARG BASE_URL=https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/${MAVEN_VERSION}

RUN mkdir -p /var/jenkins_home/apache-maven && curl -fsSL -o /var/jenkins_home/apache-maven.tar.gz ${BASE_URL}/apache-maven-${MAVEN_VERSION}-bin.tar.gz && tar -xzf /var/jenkins_home/apache-maven.tar.gz -C /var/jenkins_home/apache-maven --strip-components=1 && rm -f /var/jenkins_home/apache-maven.tar.gz
