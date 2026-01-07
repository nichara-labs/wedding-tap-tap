{ pkgs, lib, ... }:
let
  mkScript =
    let
      name = "script";
    in
    cmd:
    ''${
      pkgs.writeShellApplication {
        inherit name;
        text = ''
          ${cmd}
        '';
      }
    }/bin/${name} "$@"'';

in
{
  scripts = {
    tf.exec = mkScript ''
      set -euo pipefail
      cd "$DEVENV_ROOT/iac"

      cmd="$1"
      env="$2"
      export AWS_PROFILE="$env"

      s3_state_bucket="$(gh variable get "''${env^^}"_S3_STATE_BUCKET)"
      tofu_args=(
        -var "s3_state_bucket=''${s3_state_bucket}"
      )

      tofu init -reconfigure "''${tofu_args[@]}"
      tofu "$cmd" "''${tofu_args[@]}" "''${@:3}"
    '';
  };

}
