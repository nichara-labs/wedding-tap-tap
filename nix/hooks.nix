{
  pkgs,
  config,
  ...
}:

{
  git-hooks.hooks =
    let
      mkBash =
        let
          name = "script";
        in
        cmd:
        ''${
          # Fixes issues with set -euo not being set in hooks with bash -c
          pkgs.writeShellApplication {
            inherit name;
            text = ''${cmd}'';
          }
        }/bin/${name} "$@"''; # Passthrough caller arguments
      backend-python = "backend/.*\\.py$";
      mkBackendPython = cmd: {
        enable = true;
        entry = mkBash "cd backend; ${cmd}";
        pass_filenames = false;
        files = backend-python;
      };

      # Prefer using the bundled (devenv) version of tools for hooks, instead of installing in package managers.
      check-jsonschema = "${pkgs.check-jsonschema}/bin/check-jsonschema";
      pnpm = "${pkgs.pnpm}/bin/pnpm";
      pyright = "${pkgs.pyright}/bin/pyright";
      ruff = "${pkgs.ruff}/bin/ruff";
      tflint = "${pkgs.tflint}/bin/tflint";
      tofu = "${pkgs.opentofu}/bin/tofu";
      uv = "${pkgs.uv}/bin/uv";
    in
    {
      # Common
      trim-trailing-whitespace.enable = true;
      end-of-file-fixer.enable = true;
      check-yaml.enable = true; # Does not validate schema
      check-added-large-files.enable = true;
      check-case-conflicts.enable = true;
      shellcheck.enable = true;
      actionlint.enable = true;
      trufflehog.enable = true;
      check-terraform = {
        enable = true;
        pass_filenames = false;
        files = "\\.tf$";
        # Use .tflint.hcl in the root of the repo https://github.com/terraform-linters/tflint/blob/master/docs/user-guide/working-directory.md
        entry = mkBash ''${tflint} --init && ${tflint} --chdir=iac --recursive --config="$(realpath .tflint.hcl)"'';
      };
      update-terraform-lockfile = {
        enable = true;
        pass_filenames = false;
        files = "^iac/.*\.tf$";
        entry = mkBash ''cd iac && ${tofu} init --backend=false && ${tofu} validate'';
      };

      # Backend
      uv-sync = {
        enable = true;
        pass_filenames = false;
        files = "^backend/(pyproject.toml|uv.lock)$";
        entry = mkBash "cd backend; ${uv} sync";
      };
      ruff = mkBackendPython "${ruff} check --fix && ${ruff} format";
      # pyright: run on all files, since new errors could occur in untouched files
      pyright =
        (mkBackendPython "${pyright} --pythonpath ${config.env.DEVENV_STATE}/venv/bin/python")
        // {
          after = [ "uv-sync" ];
        };
      generate-settings-schema = mkBackendPython "${uv} run scripts/schema.py schema.json";
      validate-settings = {
        enable = true;
        entry = "${check-jsonschema} --schemafile backend/schema.json";
        files = "\\.env\\.ya?ml$";
        after = [ "generate-settings-schema" ];
      };

      # Frontend
      pnpm-install = {
        enable = true;
        entry = mkBash ''cd frontend && ${pnpm} install --frozen-lockfile'';
        pass_filenames = false;
        files = "^frontend/(package.json|pnpm-lock.yaml)$";
      };
      regenerate-ts-schema = {
        enable = true;
        entry = "scripts/openapi.sh";
        after = [ "generate-settings-schema" ];
        pass_filenames = false;
        files = backend-python;
      };
      biome = {
        enable = true;
        types_or = [
          "javascript"
          "jsx"
          "ts"
          "tsx"
          "json"
          "css"
        ];

        excludes = [
          "schema.d.ts"
          "^backend/schema.json$"
        ];
      };
      # tsc: run on all files, since new errors could occur in untouched files
      tsc = {
        enable = true;
        entry = mkBash ''cd frontend && pnpm exec next typegen && pnpm exec tsc --noEmit'';
        pass_filenames = false;
        files = "^frontend/src/.*\\.tsx?$";
      };
    };
}
