---
title: Using the API
section: Automation
summary: Sign in from a script, then list nodes, send commands, start playbooks and read the results.
---
Everything the web UI does goes through an HTTP API, so a script can do the same. Sign in, keep the token, and call the routes below.

## Find the API

Through the bundled proxy the base URL is `https://<your server>/api`. Versioned routes have `/api` twice, as in `/api/api/v1/nodes`, because the proxy strips the first one before the request reaches the server.

Every route and field is in [`backend/docs/swagger.json`](https://github.com/uptime-lab/orchestrator/blob/main/backend/docs/swagger.json) in the release tree. A production server does not serve a browsable API page.

## Sign in and get a token

```sh
API=https://orchestrator.example.com/api
read -rs PASSWORD
LOGIN=$(printf '{"email":"automation@example.com","password":"%s"}' "$PASSWORD" |
  curl -fsS -X POST "$API/auth/login" -H 'Content-Type: application/json' -d @-)
TOKEN=$(jq -r .data.access_token <<<"$LOGIN")
REFRESH=$(jq -r .data.refresh_token <<<"$LOGIN")
```

Piping the body keeps the password out of the process list. Send the token as `Authorization: Bearer $TOKEN`. It lasts 15 minutes. Exchange the refresh token for a new pair before then:

```sh
NEXT=$(printf '{"refresh_token":"%s"}' "$REFRESH" |
  curl -fsS -X POST "$API/auth/refresh" -H 'Content-Type: application/json' -d @-)
```

A 202 answer means sign-in is not finished. With `two_factor_required`, send the `two_factor_token` and an authenticator code to `POST /api/auth/2fa`. With `account selection required`, the user belongs to several accounts, so send the `pre_token` and one `account_id` to `POST /api/auth/select-account`.

There are no long-lived API keys in this release. A script signs in as a member. Create a dedicated member for it and give it the smallest role that does the job ([Team and security](../team-and-security/)). Reboots, identify and plain playbooks need **Manager**. Scripts, privileged playbooks and reading script output need **Admin**. The audit trail needs **Super Admin**.

The tokens under **Secrets** → **Tokens** enrol new devices. They do not sign in to the API.

## List nodes

```sh
curl -fsS "$API/api/v1/nodes?search=bench&page=1&per_page=50" \
  -H "Authorization: Bearer $TOKEN" | jq '.data.nodes[] | {id, name, status, ipv4}'
```

Add `ou_id=<unit-id>` for the nodes directly in a unit.

## Run something on a node

Blink the node's LED:

```sh
curl -fsS -X POST "$API/api/v1/nodes/<node-id>/identify" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"duration_sec":60}'
# {"success":true,"data":{"command_id":"<command-id>","duration_sec":60},...}
```

Run a script, then poll its command:

```sh
CMD=$(curl -fsS -X POST "$API/api/v1/nodes/<node-id>/command" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"command":"run_script","params":{"script":"df -h /","timeout_seconds":30}}' |
  jq -r .data.command_id)

curl -fsS "$API/api/v1/node-commands/$CMD" -H "Authorization: Bearer $TOKEN" |
  jq '.data | {status, result}'
# {"status":"success","result":{"exit_code":"0","stdout":"Filesystem ...","stderr":""}}
```

`status` moves through `registered`, `sent` and `in_progress`. It ends as `success`, `failed`, `superseded`, `expired` or `skipped`. A non-zero exit code fails the command. The other commands and their parameters are in the [device commands reference](https://github.com/uptime-lab/orchestrator/blob/main/docs/DEVICE-COMMANDS.md).

## Start a playbook and read the run

Find the playbook's id, then start it on the nodes you name:

```sh
curl -fsS "$API/api/v1/workflow-templates?name=Nightly" -H "Authorization: Bearer $TOKEN" |
  jq '.data[] | {id, name}'

RUN=$(curl -fsS -X POST "$API/api/v1/workflow-executions" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"template_id":"<playbook-id>","node_ids":["<node-id>"]}' | jq -r .data.id)

curl -fsS "$API/api/v1/workflow-executions/$RUN" -H "Authorization: Bearer $TOKEN" |
  jq '.data | {status, nodes: [.nodes[] | {node_id, status, error_message}]}'
```

To run it on a unit, list the unit's nodes with `ou_id` and pass their ids. A run ends as `completed`, `failed` or `partially_failed`. A draft playbook answers 409.

## Read what happened

```sh
curl -fsS "$API/api/v1/audit-events?action=node.delete&per_page=50" \
  -H "Authorization: Bearer $TOKEN" | jq '.data.events[] | {created_at, action, actor_user_id, target_id}'
```

The audit trail filters by `action` and `actor` but not by time. For device commands since a moment, set `SINCE` to an RFC3339 time:

```sh
curl -fsS "$API/api/v1/fleet/activity?since=$SINCE&status=failed" \
  -H "Authorization: Bearer $TOKEN" | jq '.data.activity[] | {created_at, node_name, slug, status}'
```

## Confirm it's you

Routes that change who can sign in or what a member may do need an `X-Reauth-Ticket` header. These include inviting members, changing roles and the security settings. Get a ticket by sending the password again:

```sh
TICKET=$(printf '{"password":"%s"}' "$PASSWORD" |
  curl -fsS -X POST "$API/api/v1/users/me/reauth/password" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' -d @- |
  jq -r .data.ticket)
```

The ticket lasts five minutes and works for several requests from the same session. Without it those routes answer 403 with `"code": "reauth_required"`.

## What limits apply

- Too many failed sign-ins from one address answer 429 with `login_throttled` and a `Retry-After` header.
- A user holds at most 10 sessions, and each sign-in past that ends the oldest one. Reuse and refresh the token instead of signing in on every call.
- The API allows 20 requests per second per account, with bursts of 100.
- Most lists page with `page` and `per_page` (default 50, at most 200).
- Errors carry `success: false`, a `message` and sometimes a `code` to act on.
