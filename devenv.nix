{
  pkgs,
  config,
  lib,
  ...
}:

{
  imports = [
    nix/hooks.nix
    nix/scripts.nix
    nix/processes.nix
  ];

  env.TF_CMD = "tofu";
  env.AWS_PROFILE = "prod";

  # https://devenv.sh/packages/
  packages = with pkgs; [
    awscli2
    opentofu
    tflint
    stripe-cli
    yq-go
  ];

  languages.python = {
    enable = true;
    directory = "./backend";
    package = pkgs.python314;
    uv.enable = true;
    uv.sync.enable = true;
  };

  languages.javascript = {
    enable = true;
    corepack.enable = true;
    pnpm.install.enable = true;
    directory = "./frontend";

  };

  enterShell = lib.mkIf (!config.devenv.isTesting) ''
    export TF_PLUGIN_CACHE_DIR=~/.tofu.d/plugin-cache
    mkdir -p "$TF_PLUGIN_CACHE_DIR"

    if [[ -z "$GITHUB_ACTIONS" ]] && ! gh auth status >/dev/null 2>&1; then
      gh auth login
    fi

    . ${config.env.DEVENV_STATE}/venv/bin/activate
  '';
}
