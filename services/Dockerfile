FROM alpine:latest

RUN apk add --no-cache git make musl-dev go

# Configure Go
ENV GOROOT /usr/lib/go
ENV GOPATH /go
ENV PATH /go/bin:$PATH

RUN mkdir -p ${GOPATH}/src ${GOPATH}/bin

WORKDIR $GOPATH

COPY . /services/
WORKDIR /services/onionscan

# configure onionscan
RUN go get github.com/HouzuoGuo/tiedot
RUN go get golang.org/x/crypto/openpgp
RUN go get golang.org/x/net/proxy
RUN go get golang.org/x/net/html
RUN go get github.com/rwcarlsen/goexif/exif
RUN go get github.com/rwcarlsen/goexif/tiff
RUN go get github.com/s-rah/onionscan

RUN echo '@edge http://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories && \
    apk -U upgrade && \
    apk -v add tor@edge curl && \
    chmod 700 /var/lib/tor && \
    rm -rf /var/cache/apk/* && \
    tor --version

COPY torrc /etc/tor/

EXPOSE 9050 9051 9053 8888

HEALTHCHECK --timeout=10s --start-period=60s \
    CMD curl --fail --socks5-hostname localhost:9050 -I -L 'https://www.facebookcorewwwi.onion/' || exit 1

CMD ["/usr/bin/tor", "-f", "/etc/tor/torrc"]
# EXPOSE 8080

# CMD ["onionscan", "--mode=analysis", "--webport=8888", "--verbose", "--torProxyAddress=proxy:9050"]