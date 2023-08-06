import knockout
from daemonize import Daemonize

PIDFILE='/var/run/sagemaker_knockout.pid'

if __name__ == "__main__":
  daemon = Daemonize(app="sagemaker_knockout", pid=PIDFILE, action=knockout.main)
  daemon.start()
