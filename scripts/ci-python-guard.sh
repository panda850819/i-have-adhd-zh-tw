#!/usr/bin/env bash
# Fail loudly unless the pinned lab CI Python is installed and self-contained: version equals
# .python-version, the build matches config/ci-python.lock, and libpython (if shared) loads from
# the same install. --github-path puts it first on PATH for later steps; --check-path fails unless
# python3 on PATH is it. Never downloads.
# Copied from panda850819/personal-infra scripts/ci-python-guard.sh; lab installs it with that repo's scripts/ci-python-install.py.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd -P)"
version_file="${CI_PYTHON_VERSION_FILE:-$repo/.python-version}"
lock_file="${CI_PYTHON_LOCK_FILE:-$repo/config/ci-python.lock}"

fail() {
  echo "::error::ci-python-guard: $*" >&2
  exit 1
}

[ -r "$version_file" ] || fail "cannot read $version_file"
[ -r "$lock_file" ] || fail "cannot read $lock_file"
pin="$(tr -d '[:space:]' <"$version_file")"
[[ "$pin" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail "$version_file must hold an exact X.Y.Z version, got '$pin'"
tag="$(sed -n 's/^PBS_TAG=//p' "$lock_file")"
sha="$(sed -n 's/^PBS_SHA256=//p' "$lock_file")"
[ -n "$tag" ] && [ -n "$sha" ] || fail "$lock_file needs PBS_TAG and PBS_SHA256"

root="${CI_PYTHON_ROOT:-/usr/local/ci-python/$pin}"
py="$root/bin/python3"
[ -x "$py" ] || fail "pinned Python $pin not installed at $root (CI does not download Python; installed by personal-infra scripts/ci-python-install.py)"

stamp="$(cat "$root/.ci-python-source" 2>/dev/null || true)"
[ "$stamp" = "cpython-$pin+$tag sha256:$sha" ] || fail "$root is build '$stamp', lock wants cpython-$pin+$tag sha256:$sha"

got="$(env -i "$py" -c 'import platform; print(platform.python_version())')" || fail "$py does not run"
[ "$got" = "$pin" ] || fail "$py is Python $got, pinned $pin"
prefix="$(env -i "$py" -c 'import sys; print(sys.base_prefix)')" || fail "$py does not run"
[ "$(cd "$prefix" && pwd -P)" = "$(cd "$root" && pwd -P)" ] || fail "$py runs from prefix $prefix, not $root"

if [ "$(uname -s)" = Linux ]; then
  deps="$(env -i ldd "$py")" || fail "ldd $py failed"
  lib="$(printf '%s\n' "$deps" | awk '/libpython/ && !seen++ { for (i = 1; i <= NF; i++) if ($i ~ /^\//) { print $i; exit } }')"
  case "$deps" in *libpython*) [ -n "$lib" ] || fail "$py needs libpython but ldd cannot resolve it" ;; esac
  if [ -n "$lib" ]; then
    lib="$(readlink -f "$lib")"
    case "$lib" in
      "$(cd "$root" && pwd -P)"/*) ;;
      *) fail "$py loads libpython from $lib, not from $root" ;;
    esac
  fi
fi
env -i "$py" -c 'import ssl, sqlite3, ctypes, venv' || fail "$py cannot import ssl/sqlite3/ctypes/venv"

echo "ci-python-guard: Python $got at $root (build $tag, libpython: ${lib:-static})"
case "${1:-}" in
  --github-path)
    [ -n "${GITHUB_PATH:-}" ] || fail "--github-path needs GITHUB_PATH"
    echo "$root/bin" >>"$GITHUB_PATH"
    ;;
  --check-path)
    on_path="$(command -v python3 || true)"
    [ "$on_path" = "$py" ] || fail "python3 on PATH is '$on_path', not $py"
    # Same checks under the job's real environment (PYTHONHOME/PYTHONPATH/LD_LIBRARY_PATH included).
    live="$(python3 -c 'import platform, sys; print(platform.python_version(), sys.base_prefix)')" || fail "python3 does not run"
    [ "$live" = "$pin $prefix" ] || fail "python3 in the job environment is '$live', want '$pin $prefix'"
    echo "ci-python-guard: python3 on PATH is $py"
    ;;
  "") ;;
  *) fail "unknown option '$1'" ;;
esac
