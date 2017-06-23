# Elasticsearch health with collectd
Elasticsearch has verbal statuses collectd cannot understand, this turns verbal to numerical. This makes life easier for your metrics and alerting platforms.

# Configuration
```
<Plugin python>
  ModulePath "<collectd plugin path>"
  Import "collectd_elastic_status_python"

	<Module collectd_elastic_status_python>
		Host "<target elastic node (default localhost)>"
		Port "<elastic port (default 9200)>"
	</Module>
</Plugin>
```
