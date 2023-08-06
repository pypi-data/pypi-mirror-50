from firebase.firebase import FirebaseApplication
from requests import Session

from hackernewslib.exceptions import InvalidItemContents
from hackernewslib.loaders import Loader
from hackernewslib.schemas import ItemSchema, UserSchema
from hackernewslib.models import User, Content


def create_client(api_url="https://hacker-news.firebaseio.com"):
    app = FirebaseApplication(api_url, None)
    session = Session()

    return HackernewsFirebaseClient(app, session)


class HackernewsFirebaseClient(object):
    def __init__(self, app, session):
        self.app = app
        self.session = session

        self.item_schema = ItemSchema()
        self.user_schema = UserSchema()
        self.loader = Loader()

    @property
    def api_url(self):
        return self.app.dsn

    def download(self, url):
        response = self.session.get(url, timeout=5, verify=False)

        return Content(
            url=url,
            response=response
        )

    def max_item(self):
        return self.app.get("/v0//maxitem", None)

    def item(self, item_id):
        item_data = self.app.get("/v0//item", item_id)
        if item_data is None:
            return None

        deserialization_result = self.item_schema.load(item_data)
        if deserialization_result.errors:
            raise InvalidItemContents(
                data=item_data,
                errors=deserialization_result.errors
            )

        return self.loader.load(self, deserialization_result.data)

    def items(self, item_ids):
        for item_id in item_ids:
            item = self.item(item_id)

            yield item

    def user(self, username):
        user_data = self.app.get("/v0//user", username)
        if user_data is None:
            return None

        deserialization_result = self.user_schema.load(user_data)
        if deserialization_result.errors:
            raise InvalidItemContents(
                data=user_data,
                errors=deserialization_result.errors
            )

        return User(client=self, **deserialization_result.data)

    def _group_story_ids(self, story_group):
        return self.app.get(story_group, None)

    def _group_stories(self, story_group, max_stories=None):
        story_ids = self._group_story_ids("/v0/{}".format(story_group))
        if max_stories:
            story_ids = story_ids[:max_stories]

        return self.items(story_ids)

    def new(self, max_stories=None):
        return self._group_stories(
            story_group="newstories",
            max_stories=max_stories
        )

    def top(self, max_stories=None):
        return self._group_stories(
            story_group="topstories",
            max_stories=max_stories
        )

    def best(self, max_stories=None):
        return self._group_stories(
            story_group="beststories",
            max_stories=max_stories
        )

    def ask(self, max_stories=None):
        return self._group_stories(
            story_group="askstories",
            max_stories=max_stories
        )

    def show(self, max_stories=None):
        return self._group_stories(
            story_group="showstories",
            max_stories=max_stories
        )

    def job(self, max_stories=None):
        return self._group_stories(
            story_group="jobstories",
            max_stories=max_stories
        )

    def updates(self):
        return self.app.get("/v0//updates", None)
