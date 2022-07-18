# smspilot

Web-hook for [smspilot.ru](https://smspilot.ru) (SP) service.

## Requirements

- Python 3.6+
- [thttpd](https://acme.com/software/thttpd/) (or other CGI-powered HTTP server; not tested)

Works on CentOS 7+, macOS 10.15

## Install

1. Install thttpd
2. Patch its default config (`/etc/thttpd.conf`) like this:

   ```diff
   -chroot
   +nochroot
   +port=58080
   +charset=utf-8
   +cgipat=/*.py
   ```

3. As `thttpd` runs with user `thttpd` privileges make sudoer file (`/etc/sudoers.d/thttpd`) like this:

   ```
   thttpd localhost=/usr/local/bin/virsh_wrapper.sh NOPASSWD:/usr/local/bin/virsh_wrapper.sh
   ```

5. Copy `smspilot.py` and `sms.py` into `/var/www/thttpd/`
6. Create `/etc/smspilot.conf` like the [sample](smspilot_sample.json)

## Usage

SP sends HTTP POST request with urlencoded values:

- `id`: int, something automatic; not used now
- `num`: int, SP's service phone number what SMS send to
- `phone`: int, phone number what SMS send from
- `user_id`: int, SP contract number
- `message`: str, code of 'command' to execute (see [sample](smspilot_sample.json) for details)

Response must be any string (including empty) but 'HTTP/1.1 200 OK' is preferable.

## Test

Run builtin CGI server (`python3 smspilot.py`)
and make test requests to them (`./test.sh`)
