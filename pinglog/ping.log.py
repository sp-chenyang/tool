#!/usr/bin/env python

import sys, time
from daemon import Daemon

import datetime
import subprocess

class MyDaemon(Daemon):
    def run(self):
        while True:
            with open('/tmp/ping.log.txt', 'a+b') as logfile:
                ping = subprocess.Popen(['ping', '-c1', '-w4', 'www.xuanran001.com'], stdout=logfile)
                time.sleep(5)
                # Not strictly necessary, but it avoids signaling for no reason
                if ping.poll() is None:
                    ping.kill()
                    ping.wait()

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)



