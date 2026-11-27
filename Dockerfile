# SPDX-License-Identifier: Apache-2.0
# Official multi-platform index pins, not architecture-specific manifests.
FROM python:3.13.18-slim-trixie@sha256:7249d5587b78209a006dc4a3b5340678f84ea729239193aa559962cd8c1fce50 AS common
# Fixed signed Debian archives; do not fall back to floating repositories.
RUN set -eu; \
    rm -f /etc/apt/sources.list /etc/apt/sources.list.d/debian.sources; \
    printf '%s\n' \
      'deb [check-valid-until=no] https://snapshot.debian.org/archive/debian/20261127T000000Z/ trixie main' \
      'deb [check-valid-until=no] https://snapshot.debian.org/archive/debian/20261127T000000Z/ trixie-updates main' \
      'deb [check-valid-until=no] https://snapshot.debian.org/archive/debian-security/20261127T000000Z/ trixie-security main' \
      > /etc/apt/sources.list; \
    apt-get -o APT::Update::Error-Mode=any update; \
    apt-get install -y --no-install-recommends --only-upgrade passwd libzstd1; \
    rm -rf /var/lib/apt/lists/*; \
    python3 -m pip uninstall -y pip; \
    rm -rf /usr/local/lib/python3.13/ensurepip; \
    python3 -c "import sys,importlib.util,sqlite3,ssl; assert sys.version_info[:3] == (3,13,18); assert all(importlib.util.find_spec(n) is None for n in ('pip','ensurepip','setuptools','msgpack','urllib3')); print(sqlite3.sqlite_version, ssl.OPENSSL_VERSION)"

FROM common AS verification
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOME=/tmp TMPDIR=/tmp
RUN groupadd --gid 10001 etis && useradd --uid 10001 --gid 10001 --no-create-home --home-dir /tmp etis
# Verification does not need the vulnerable terminfo inspection CLI. Keep its
# package metadata and libraries intact; scanners must still report advisories.
RUN set -eu; \
    rm -f /usr/bin/infocmp; \
    find /usr -xdev -type f -perm /6000 -exec chmod a-s {} +; \
    remaining="$(find /usr -xdev -type f -perm /6000 -print)"; \
    test -z "$remaining"; test ! -e /usr/bin/infocmp
WORKDIR /opt/etis
# Context is deliberately allowlisted by .dockerignore. Source stays root-owned.
COPY . .
RUN chmod -R a+rX,go-w /opt/etis
USER 10001:10001
CMD ["python3", "containers/verify.py"]

# Minimal tooling for editable development and VS Code bootstrap.
FROM common AS development
RUN apt-get -o APT::Update::Error-Mode=any update && apt-get install -y --no-install-recommends make curl libstdc++6 \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -c 'import shutil,subprocess; assert shutil.which("git") is None; packages=subprocess.check_output(["dpkg-query","-W","-f=${Package} ${db:Status-Status}\n"],text=True).splitlines(); assert "libexpat1 installed" not in packages'
ARG ETIS_DEV_UID=1000
ARG ETIS_DEV_GID=1000
RUN set -eu; \
    test "$ETIS_DEV_UID" -gt 0; test "$ETIS_DEV_GID" -gt 0; \
    if ! getent group "$ETIS_DEV_GID" >/dev/null; then groupadd --gid "$ETIS_DEV_GID" etis; fi; \
    useradd --uid "$ETIS_DEV_UID" --gid "$ETIS_DEV_GID" --create-home --shell /bin/bash etis; \
    install -d -o "$ETIS_DEV_UID" -g "$ETIS_DEV_GID" -m 0750 /state; \
    touch /state/.etis-state; chown "$ETIS_DEV_UID:$ETIS_DEV_GID" /state/.etis-state; \
    find /usr -xdev -type f -perm /6000 -exec chmod a-s {} +; \
    remaining="$(find /usr -xdev -type f -perm /6000 -print)"; \
    test -z "$remaining"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOME=/home/etis TMPDIR=/tmp
WORKDIR /workspace
USER etis
CMD ["sleep", "infinity"]

# Plain docker build selects the smaller verification image, not development.
FROM verification AS final
