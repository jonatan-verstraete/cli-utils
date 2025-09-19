


:cpr() {

  get_repo_path() {
    local github_dir="$HOME/Documents/GitHub/bricsys247"
    local key="$1"
    if [[ -z "$key"  ]]; then
      echo "$github_dir-frontend"
      return 0
    fi

    case "$key" in
      pkg)
        echo "$github_dir-frontend-packages";;
      dome)
        echo "$github_dir-dome-frontend-react";;
      trans)
        echo "$github_dir-translations-api";;
      comp)
        echo "$github_dir-react-components";;
      viewer)
        echo "$github_dir-viewers-frontend";;
      front)
        echo "$github_dir-frontend" ;;
      *)
        echo "$github_dir-$key"
        ;;
    esac
  }


  local type=$1
  local ticket=$2
  local draft=false
  local open=false
  local repo_key=""
  local default_repo_key  # unused but might be needed
  local github_dir="$HOME/Documents/GitHub"
  local original_dir="$PWD"
  shift 2
  local gh_args=()
  local description

  # Check for help
  if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: cpr <type> <ticket> [options]"
    echo "Type: bug, ft, us (case insensitive, outputs as BUG, FT, US)"
    echo "Options:"
    echo "  -d            Create as draft"
    echo "  -r <key>      Specify repo key (default: $default_repo_key)"
    echo "  -o            Open PR in browser"
    echo "  --help        Show this help message"
    echo "  Any other args are passed to gh pr create"
    echo "Repo keys: default (add more in get_repo_path function)"
    return 0
  fi

  # Ensure type and ticket are provided
  if [[ -z "$type" || -z "$ticket" ]]; then
    echo "Error: Type and ticket are required"
    return 1
  fi

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -d)
        draft=true
        shift
        ;;
      -r)
        repo_key="$2"
        shift 2
        ;;
      -o)
        open=true
        shift
        ;;
      *)
        gh_args+=("$1")
        shift
        ;;
    esac
  done

  # Set default repo key if none provided
  if [[ -z "$repo_key" ]]; then
    repo_key="$default_repo_key"
  fi

  # Get repo path
  local repo_path
  repo_path=$(get_repo_path "$repo_key")

  # Validate repo path
  if [[ -z "$repo_path" ]]; then
    echo "Error: Unknown repo key '$repo_key'"
    return 1
  fi
  if ! [ -d "$repo_path" ]; then
    echo "Error: Repo path '$repo_path' does not exist"
    return 1
  fi
  if ! [ -d "$repo_path/.git" ]; then
    echo "Error: '$repo_path' is not a Git repository"
    return 1
  fi

  # Validate type
  case "$(echo "$type" | tr '[:upper:]' '[:lower:]')" in
    bug|ft|us)
      type=$(echo "$type" | tr '[:lower:]' '[:upper:]')
      ;;
    *)
      echo "Error: Type must be one of: bug, ft, us"
      return 1
      ;;
  esac

  # Prompt for description
  echo "Enter PR description (optional, press Enter to skip):"
  read -r description

  if [[ -z "$description" ]]; then
    description="- [ ]"
  fi

  description="$description"$'\n\n'"Contributes AB#$ticket"

  # Compose title
  local title="$type/$ticket"

  # Navigate to repo
  cd "$repo_path" || {
    echo "Error: Failed to navigate to '$repo_path'"
    return 1
  }

  # Create PR with gh
  gh pr create \
    --title "$title" \
    --body "$description" \
    $( [[ "$draft" == true ]] && echo "--draft" ) \
    "${gh_args[@]}"

  local pr_status=$?

  # Open PR in browser if requested
  if [[ "$open" == true && $pr_status -eq 0 ]]; then
    gh pr view --web
  fi

  # Return to original directory
  cd "$original_dir" || {
    echo "Warning: Failed to return to '$original_dir'"
  }

  return $pr_status
}


cpr() {
  local type=$1
  local ticket=$2
  local draft=false
  local open=false
  local repo_key=""
  local default_repo_key="default"
  local github_dir="$HOME/Documents/GitHub"
  local original_dir="$PWD"
  local head_branch=""
  shift 2
  local gh_args=()

  # Check for help
  if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: cpr <type> <ticket> [options]"
    echo "Type: bug, ft, us (case insensitive, outputs as BUG, FT, US)"
    echo "Options:"
    echo "  -d            Create as draft"
    echo "  -r <key>      Specify repo key (default: $default_repo_key)"
    echo "  -o            Open PR in browser"
    echo "  --head <branch>  Specify head branch (required)"
    echo "  --help        Show this help message"
    echo "  Other args passed to gh pr create (e.g., --base, --label)"
    echo "Repo keys: default (add more in get_repo_path function)"
    return 0
  fi

  # Ensure type and ticket are provided
  if [[ -z "$type" || -z "$ticket" ]]; then
    echo "Error: Type and ticket are required"
    return 1
  fi

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -d)
        draft=true
        shift
        ;;
      -r)
        repo_key="$2"
        shift 2
        ;;
      -o)
        open=true
        shift
        ;;
      --head)
        head_branch="$2"
        gh_args+=("--head" "$2")
        shift 2
        ;;
      *)
        gh_args+=("$1")
        shift
        ;;
    esac
  done

  # Validate head branch
  if [[ -z "$head_branch" ]]; then
    echo "Error: Head branch must be specified with --head"
    return 1
  fi

  # Set default repo key if none provided
  if [[ -z "$repo_key" ]]; then
    repo_key="$default_repo_key"
  fi

  # Get repo path
  local repo_path
  repo_path=$(get_repo_path "$repo_key")

  # Validate repo path
  if [[ -z "$repo_path" ]]; then
    echo "Error: Unknown repo key '$repo_key'"
    return 1
  fi
  if ! [ -d "$repo_path" ]; then
    echo "Error: Repo path '$repo_path' does not exist"
    return 1
  fi
  if ! [ -d "$repo_path/.git" ]; then
    echo "Error: '$repo_path' is not a Git repository"
    return 1
  fi

  # Validate type
  case "$(echo "$type" | tr '[:upper:]' '[:lower:]')" in
    bug|ft|us)
      type=$(echo "$type" | tr '[:lower:]' '[:upper:]')
      ;;
    *)
      echo "Error: Type must be one of: bug, ft, us"
      return 1
      ;;
  esac

  # Prompt for description
  echo "Enter PR description (optional, press Enter to skip):"
  read -r description

  if [[ -z "$description" ]]; then
    description="- [ ]"
  fi

  description="$description"$'\n\n'"Contributes AB#$ticket"

  # Compose title
  local title="$type/$ticket"

  # Navigate to repo
  cd "$repo_path" || {
    echo "Error: Failed to navigate to '$repo_path'"
    return 1
  }

  # Ensure the head branch exists locally and is pushed
  if ! git show-ref --quiet --verify "refs/heads/$head_branch"; then
    echo "Creating branch '$head_branch'"
    git checkout -b "$head_branch" || {
      echo "Error: Failed to create branch '$head_branch'"
      cd "$original_dir"
      return 1
    }
  else
    git checkout "$head_branch" || {
      echo "Error: Failed to checkout branch '$head_branch'"
      cd "$original_dir"
      return 1
    }
  fi

  # Push the branch to ensure it’s on the remote
  git push origin "$head_branch" --force || {
    echo "Warning: Failed to push branch '$head_branch' to origin"
  }

  # Create PR with gh
  echo "Creating PR: title='$title', head='$head_branch', repo='$repo_path'"
  gh pr create \
    --title "$title" \
    --body "$description" \
    $( [[ "$draft" == true ]] && echo "--draft" ) \
    "${gh_args[@]}"

  local pr_status=$?

  # Open PR in browser if requested
  if [[ "$open" == true && $pr_status -eq 0 ]]; then
    gh pr view --web
  fi

  # Return to original directory
  cd "$original_dir" || {
    echo "Warning: Failed to return to '$original_dir'"
  }

  return $pr_status
}