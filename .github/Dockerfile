FROM alpine

# Install necessary packages
RUN apk -v --no-cache --update add \
        nodejs \
        npm \
        python3 \
        ca-certificates \
        groff \
        less \
        bash \
        make \
        curl \
        wget \
        zip \
        git \
        py3-pip \
        && update-ca-certificates && \
    npm install -g aws-cdk

# Set the working directory
WORKDIR /opt/app

# Copy the entire project directory to the Docker image
COPY . /opt/app/

# Ensure setup.sh is executable
RUN chmod +x /opt/app/.github/setup.sh

# Set default command to check CDK version
CMD ["cdk", "--version"]

