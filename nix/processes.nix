{
  lib,
  config,
  ...
}:
{
  # This guard doesn't work for some reason (isTesting is false even with devenv test)
  processes = lib.mkIf (!config.devenv.isTesting) {
    frontend = {
      exec = "pnpm dev";
      cwd = "./frontend";
    };
    backend = {
      exec = "fastapi dev";
      cwd = "./backend";
    };
  };
}
