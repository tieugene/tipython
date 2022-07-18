"""Smspilot web-hook"""
import os
import json
import logging
import logging.handlers
import cgi
import platform
from http.server import HTTPServer, CGIHTTPRequestHandler

# const
CFG_FILE_NAME = 'smspilot.conf'
LOG_NAME = 'SMS'
# var
Cfg: dict = {}


class Rq:
    """Request payload"""
    id: int
    num: int
    phone: int
    user_id: int
    message: str

    def __str__(self):
        return f"id={self.id}, num={self.num}, phone={self.phone}, user_id={self.user_id}, message='{self.message}'"


class SmsPilotError(RuntimeError):
    """Basic error"""
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg


def prepare_log():
    """Open logger
    :todo: handle loglevel
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s(SMS): %(msg)s",
        handlers=(
            logging.StreamHandler(),
            logging.handlers.SysLogHandler(
                address='/var/run/syslog' if platform.system() == 'Darwin' else '/dev/log'
            )
        )
    )


def load_cfg():
    """Load config
    :todo: try/except json.decoder.JSONDecodeError
    """
    def __inner(path: str):
        """Laod config file"""
        if os.path.isfile(path):
            with open(path, 'rt', encoding='utf-8') as file:
                Cfg.update(json.load(file))

    __inner(os.path.join('/etc', CFG_FILE_NAME))
    __inner(os.path.expanduser('~/.' + CFG_FILE_NAME))
    for name in ('num', 'phone', 'user_id', 'message', 'cmd'):
        if name not in Cfg:
            raise SmsPilotError(f"Config has no '{name}'")


def sanitize() -> Rq:
    """Sanitize POST request.
    :todo: check form values type by Rq.__annotation__
    """
    src = os.environ.get('REMOTE_ADDR')
    if src is None:
        raise SmsPilotError('Remote address absent')
    meth = os.environ.get('REQUEST_METHOD')
    if meth != 'POST':
        raise SmsPilotError(f"Bad http request method '{meth}' from '{src}'")
    form = cgi.FieldStorage()
    data = Rq()
    for fname in ('id', 'num', 'phone', 'user_id', 'message'):
        value = form.getvalue(fname)
        if fname != 'message':
            try:
                value = int(value)
            except TypeError as err:
                raise SmsPilotError(f"'{fname}' has unknown type ({value})") from err
            except ValueError as err:
                raise SmsPilotError(f"'{fname}' is not int ({value})") from err
        if fname != 'id' and value not in Cfg[fname]:
            raise SmsPilotError(f"'{fname}': unknown value '{value}'")
        data.__dict__[fname] = value
    return data


def hook():
    """The main.
    :todo: print 'HTTP/1.1. 4xx' on error
    """
    prepare_log()
    try:
        load_cfg()
        data = sanitize()
    except SmsPilotError as err:
        logging.error(err.msg)
    else:
        logging.debug(f"Request: {data}")
        command = f"{Cfg['cmd']} {Cfg['message'][data.message]} {data.phone}"
        if os.system(command) >> 8:
            logging.error("Exec err: %s", command)
        else:
            logging.debug("Exec OK: %s", command)
    print('HTTP/1.1 200 OK')  # any response required


def srv():
    """Loopback HTTP-CGI server"""
    class Handler(CGIHTTPRequestHandler):
        """Search sms.py right here"""
        cgi_directories = ['/']

    httpd = HTTPServer(("", 8000), Handler)
    print("Welcome to port", 8000)
    httpd.serve_forever()


if __name__ == '__main__':
    srv()
