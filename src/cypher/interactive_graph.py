import json

from IPython.display import display_javascript, display_html, display

class InteractiveGraph(object):
    js = """
(function() {
"use strict";

var container = $(element).toArray()[0]; // element provided by IPython

require(["//cdnjs.cloudflare.com/ajax/libs/vis/3.11.0/vis.min.js"],
function(vis) {

    var data = {
      nodes: %s,
      edges: %s
    };
    var options = {
      nodes: {
        shape: 'box'
      }
    };
    network = new vis.Network(container, data, options);
});
})();
"""

    def __init__(self, graph, label="id"):
        self._graph = graph
        self.label_prop = label

    def _ipython_display_(self):
        display_javascript(self.js % (
                json.dumps(
                    {n["id"]: {
                        "id": n["id"],
                        "properties": n["properties"],
                        "neo4jLabels": n["labels"],
                        "label": n.get(self.label_prop, n["id"])
                    } for o in self._graph
                      for n in o["nodes"]
                    }.values()),
                json.dumps(
                  {( e["startNode"], e["endNode"]): {
                        "from": e["startNode"],
                        "to": e["endNode"],
                        "label": e["type"],
                        "properties": e["properties"]
                    } for o in self._graph
                      for e in o["relationships"]
                    }.values())
            ),
                raw=True)
        return "xaaaa"
