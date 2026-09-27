#!/usr/bin/env bash

set -euo pipefail

readonly PROJECT_NAME="forge-smoke"
readonly SERVICE_NAME="api"
readonly HEALTH_URL="http://127.0.0.1:8000/health"

compose() {
  docker compose --project-name "${PROJECT_NAME}" "$@"
}

cleanup() {
  exit_code=$?
  trap - EXIT

  if ((exit_code != 0)); then
    printf '\nContainer smoke test failed. Service logs:\n' >&2
    compose logs --no-color "${SERVICE_NAME}" >&2 || true
  fi

  compose down --volumes --remove-orphans >/dev/null 2>&1 || true

  if ((exit_code == 0)); then
    printf 'Container smoke test passed; temporary resources removed.\n'
  fi

  exit "${exit_code}"
}

require_command() {
  command_name=$1
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    printf 'Required command not found: %s\n' "${command_name}" >&2
    return 1
  fi
}

trap cleanup EXIT

require_command docker
require_command curl
docker info >/dev/null
docker compose version >/dev/null

export FORGE_ENVIRONMENT="test"
export FORGE_LOG_LEVEL="WARNING"
export FORGE_LOG_JSON="true"

printf 'Validating Compose configuration...\n'
compose config --quiet

printf 'Removing stale smoke-test resources...\n'
compose down --volumes --remove-orphans >/dev/null 2>&1 || true

printf 'Building and starting Forge...\n'
compose up --build --detach --wait --wait-timeout 60

printf 'Checking the public health response...\n'
health_response=$(curl --fail --silent --show-error "${HEALTH_URL}")
if [[ "${health_response}" != '{"status":"ok"}' ]]; then
  printf 'Unexpected health response: %s\n' "${health_response}" >&2
  exit 1
fi

printf 'Checking the process identity...\n'
identity=$(
  compose exec --no-TTY "${SERVICE_NAME}" \
    sh -c 'printf "%s:%s" "$(id -u)" "$(id -g)"'
)
if [[ "${identity}" != "10001:10001" ]]; then
  printf 'Unexpected container identity: %s\n' "${identity}" >&2
  exit 1
fi

printf 'Checking settings and runtime contents...\n'
compose exec --no-TTY "${SERVICE_NAME}" python -c '
import os
import pathlib
import shutil

from forge.config import load_settings

settings = load_settings()
assert settings.environment.value == "test"
assert settings.log_level.value == "WARNING"
assert settings.log_json is True

excluded_paths = (
    "/app/.env",
    "/app/.git",
    "/app/src",
    "/app/tests",
    "/app/pyproject.toml",
)
assert not any(pathlib.Path(path).exists() for path in excluded_paths)
assert shutil.which("uv") is None
assert not os.access("/app", os.W_OK)
assert os.access("/tmp", os.W_OK)
'

printf 'Checking container security controls...\n'
container_id=$(compose ps --quiet "${SERVICE_NAME}")
if [[ -z "${container_id}" ]]; then
  printf 'Compose did not return a container ID.\n' >&2
  exit 1
fi

security_state=$(
  docker inspect \
    --format '{{.Config.User}}|{{.HostConfig.ReadonlyRootfs}}|{{json .HostConfig.CapDrop}}|{{json .HostConfig.SecurityOpt}}' \
    "${container_id}"
)
expected_security_state='10001:10001|true|["ALL"]|["no-new-privileges:true"]'
if [[ "${security_state}" != "${expected_security_state}" ]]; then
  printf 'Unexpected container security state: %s\n' "${security_state}" >&2
  exit 1
fi
