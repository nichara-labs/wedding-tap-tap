# Wedding Tap Tap Game

## Development

Requirements:

- [Nix]
- [devenv]
- [direnv]
- AWS CLI configuration for the `prod` account

<details>
<summary>AWS CLI configuration</summary>

In `~/.aws/config`, ensure the following are present:

```ini
[profile prod]
sso_session = default
sso_account_id = 412373518635
sso_role_name = AdministratorAccess
region = ap-southeast-1

[sso-session default]
sso_start_url = https://d-9667b76e76.awsapps.com/start/#
sso_region = ap-southeast-1
sso_registration_scopes = sso:account:access
```

</details>

If this is the first time the project is being run, you will need to create the necessary resources as shown by braces (`{}`) in `backend/example.env.yaml`.

To start everything, in the main directory, run:

```sh
up
```

## Production

In AWS Parameter Store, ensure that the following variables are set for the `prod` environment:

- `/infra/cloudflare/api_token` with `Zone:Edit,Zone.Single Redirect` permissions (used for updating DNS and `www` redirection rules)

Pushing to the `prod` branch will cause a deployment action.

[Nix]: https://nixos.org/download.html
[devenv]: https://devenv.sh/
[direnv]: https://direnv.net/
