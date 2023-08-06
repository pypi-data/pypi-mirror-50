from hackernewslib.models import Story, Comment, Job, Poll, Part, Raw


class Loader(object):
    def __init__(self):
        self.supported_item_types = {
            "story": Story,
            "comment": Comment,
            "job": Job,
            "poll": Poll,
            "pollopt": Part
        }

    def load(self, client, data):
        item_class = self.supported_item_types.get(data.get("type"), Raw)

        return item_class.parse(
            client=client,
            item=data
        )
