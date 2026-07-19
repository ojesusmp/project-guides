#!/usr/bin/env bash
set -euo pipefail

umask 077

repository=${PROJECT_GUIDES_REPOSITORY:-https://github.com/ojesusmp/project-guides.git}
requested_ref=${1:-${PROJECT_GUIDES_COMMIT:-}}
cache_root=${PROJECT_GUIDES_CACHE_DIR:-"$HOME/.cache/project-guides"}
skills_root=${PROJECT_GUIDES_SKILLS_DIR:-"$HOME/.agents/skills"}
target="$skills_root/project-guides"
marker_name=.project-guides-codex-cloud

fail() {
  printf 'project-guides: %s\n' "$*" >&2
  exit 1
}

command -v git >/dev/null 2>&1 || fail "git is required during the Codex Cloud setup phase"
command -v python3 >/dev/null 2>&1 || fail "python3 is required during the Codex Cloud setup phase"
[[ -n "$requested_ref" ]] || fail "provide a full 40-character commit SHA"

if [[ "$requested_ref" == main ]]; then
  [[ ${PROJECT_GUIDES_ALLOW_DEVELOPMENT_REF:-0} == 1 ]] ||
    fail "main is development-only; set PROJECT_GUIDES_ALLOW_DEVELOPMENT_REF=1 to opt in"
  commit=$(git ls-remote "$repository" refs/heads/main | awk 'NR == 1 { print $1 }')
  [[ "$commit" =~ ^[0-9a-fA-F]{40}$ ]] || fail "could not resolve main to a full commit SHA"
  printf 'project-guides: development ref main resolved to %s\n' "$commit"
else
  [[ "$requested_ref" =~ ^[0-9a-fA-F]{40}$ ]] ||
    fail "production installs require a full 40-character commit SHA"
  commit=$(printf '%s' "$requested_ref" | tr 'A-F' 'a-f')
fi

mkdir -p "$cache_root/releases" "$cache_root/staging" "$skills_root"

if [[ -e "$target" || -L "$target" ]]; then
  [[ -L "$target" ]] || fail "$target exists and is not managed by this installer"
  [[ -f "$target/$marker_name" ]] || fail "$target is a symlink without the project-guides ownership marker"
  installed_repository=$(sed -n 's/^repository=//p' "$target/$marker_name")
  [[ "$installed_repository" == "$repository" ]] ||
    fail "$target belongs to a different repository: $installed_repository"
  installed_commit=$(sed -n 's/^commit=//p' "$target/$marker_name")
  if [[ "$installed_commit" == "$commit" ]]; then
    python3 "$target/scripts/validate_project_guides.py"
    printf 'project-guides: %s is already active and valid\n' "$commit"
    exit 0
  fi
fi

stage=$(mktemp -d "$cache_root/staging/candidate.XXXXXX")
cleanup() {
  rm -rf -- "$stage"
}
trap cleanup EXIT

git -C "$stage" init --quiet repository
git -C "$stage/repository" remote add origin "$repository"
git -C "$stage/repository" fetch --quiet --depth 1 origin "$commit"
git -C "$stage/repository" checkout --quiet --detach FETCH_HEAD
resolved_commit=$(git -C "$stage/repository" rev-parse HEAD | tr 'A-F' 'a-f')
[[ "$resolved_commit" == "$commit" ]] || fail "fetched commit $resolved_commit does not match $commit"

source_skill="$stage/repository/plugins/project-guides/skills/project-guides"
[[ -f "$source_skill/SKILL.md" ]] || fail "the canonical project-guides skill is missing at commit $commit"
python3 "$source_skill/scripts/validate_project_guides.py"

release="$cache_root/releases/$commit"
if [[ ! -d "$release" ]]; then
  release_candidate="$cache_root/releases/.${commit}.$$"
  mkdir "$release_candidate"
  cp -a "$source_skill/." "$release_candidate/"
  {
    printf 'repository=%s\n' "$repository"
    printf 'commit=%s\n' "$commit"
  } > "$release_candidate/$marker_name"
  python3 "$release_candidate/scripts/validate_project_guides.py"
  mv -- "$release_candidate" "$release"
else
  [[ -f "$release/$marker_name" ]] || fail "cached release $release is missing its ownership marker"
  python3 "$release/scripts/validate_project_guides.py"
fi

link_candidate="$skills_root/.project-guides.$$.link"
rm -f -- "$link_candidate"
ln -s "$release" "$link_candidate"
mv -Tf -- "$link_candidate" "$target"

printf 'project-guides: activated %s at %s\n' "$commit" "$target"
