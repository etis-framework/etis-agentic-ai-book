#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Host-side tool; never install the scanner in the runtime images.
set -eu
out=${1:?usage: scan-images.sh NEW_EVIDENCE_DIRECTORY}
project=${COMPOSE_PROJECT_NAME:?set COMPOSE_PROJECT_NAME to the built Compose project}
[ "$(uname -s)" = Linux ]
mkdir "$out"
case $(uname -m) in
  x86_64) arch=64bit; checksum=bc0fc726e017b8927a62b2d3531d7a84ee01769daf5c99ed866dced54089fdbf ;;
  aarch64) arch=ARM64; checksum=ab9d51f86e6a5fb936f605faff6b593ac51bc378fff4d3e8b9d58358b9c367c3 ;;
  *) echo 'Unsupported Linux scanner host' >&2; exit 1 ;;
esac
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
asset=trivy_0.76.2_Linux-$arch.tar.gz
curl --fail --location --retry 3 --max-time 180 -o "$work/$asset" "https://github.com/aquasecurity/trivy/releases/download/v0.76.2/$asset"
printf '%s  %s\n' "$checksum" "$work/$asset" | sha256sum -c -
tar -xzf "$work/$asset" -C "$work" trivy
scanner=$work/trivy
"$scanner" --version > "$out/scanner.txt"
date -u >> "$out/scanner.txt"
failed=0
for target in companion dev; do
    id=$(docker image inspect --format '{{.Id}}' "$project-$target")
    docker image inspect --format '{{.Id}} {{.Os}}/{{.Architecture}} {{.Size}}' "$id" > "$out/$target-image.txt"
    docker run --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges:true "$id" dpkg-query -W > "$out/$target-packages.tsv"
    "$scanner" image --image-src docker --format cyclonedx --output "$out/$target-sbom.json" "$id"
    "$scanner" image --image-src docker --scanners vuln --format json --output "$out/$target-vulnerabilities.json" "$id"
    "$scanner" image --image-src docker --scanners vuln --severity HIGH,CRITICAL --exit-code 1 "$id" > "$out/$target-gate.txt" 2>&1 || failed=1
    cat "$out/$target-gate.txt"
done
"$scanner" --version >> "$out/scanner.txt"
exit "$failed"
