import collectd
import json
import requests
import time


_elastic_ip = "localhost"
_elastic_port = "9200"

PLUGIN_NAME = "elastic_status"
INTERVAL = 10

def configure_plugin(configobj):
        global _elastic_ip
        global _elastic_port

        collectd.info('elastic_status: Configure with: key=%s, children=%r' % (configobj.key, configobj.children))
        config = {c.key: c.values for c in configobj.children}

        _elastic_ip = next(iter(config.get("Host", "localhost")))
        _elastic_port = next(iter(config.get("Port", "9200")))


def read_status_page(data=None):
        global _elastic_ip
        global _elastic_port

        latency = 0
        status = -1
        json_data = None

        try:
                start = time.time()
                collectd.debug('http://%s:%s/_cluster/health' % (_elastic_ip, _elastic_port))
                response = requests.get('http://%s:%s/_cluster/health' % (_elastic_ip, _elastic_port), timeout=5)
                latency = time.time() - start
                json_data = response.json()
        except requests.exceptions.ConnectionError:
                collectd.error("Connection problem, cannot query http://%s:%s/_cluster/health" % (_elastic_ip, _elastic_port))
                return
        except requests.exceptions.Timeout:
                collectd.error("Elasticsearch is timing out with 5 second timeout")
                return
        except ValueError:
                collectd.error("Malformed json retrieved: %s" % json_data)
                return

        if 'status' not in json_data:
                collect.error("Status node is not present in received json")
                return

        statuses = {
                "green": 0,
                "yellow": 1,
                "red": 2
        }

        status = statuses.get(json_data["status"], -1)

        latency_gauge = collectd.Values(type='gauge', type_instance='latency')
        status_gauge = collectd.Values(type='gauge', type_instance='status')

        latency_gauge.plugin = PLUGIN_NAME
        status_gauge.plugin = PLUGIN_NAME

        latency_gauge.values = [latency]
        status_gauge.values = [status]

        latency_gauge.dispatch()
        status_gauge.dispatch()


collectd.register_config(configure_plugin)
collectd.register_read(read_status_page, INTERVAL)
