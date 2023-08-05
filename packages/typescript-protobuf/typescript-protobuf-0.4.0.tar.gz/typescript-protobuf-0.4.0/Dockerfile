FROM python:3.7

WORKDIR /work

# Install dependencies
RUN apt-get update -qqy && apt-get install -qqy --no-install-recommends wget unzip && \
  # Install needed Python dependencies.
  pip install protobuf && \
  # Install Protobuf compiler.
  PROTOBUF_VERSION=$(curl -i https://github.com/protocolbuffers/protobuf/releases/latest | grep ^Location: | sed -e "s/^.*\/v//;s/\s*$//") \
  bash -c 'wget --quiet https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOBUF_VERSION}/protoc-${PROTOBUF_VERSION}-linux-x86_64.zip -O protoc.zip' && \
  unzip -qq protoc.zip && rm protoc.zip && rm readme.txt && mv bin/protoc /usr/local/bin && mkdir /usr/local/share/proto && mv include/google /usr/local/share/proto

COPY src src