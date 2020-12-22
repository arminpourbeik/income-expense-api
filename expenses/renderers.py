import json
from rest_framework import renderers


class ExpenseRenderers(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, media_type, renderer_context):
        response = ""
        if "ErrorDetail" in str(data):
            response = json.dumps({"error": data})

        else:
            response = json.dumps({"data": data})

        return response
