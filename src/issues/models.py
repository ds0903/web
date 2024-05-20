# from typing import Any

from django.db import models
from django.db.models import Q

from shared.django import TimestampMixin
from users.models import User

ISSUE_STATUS_CGOICES = (
    (1, "OPENED"),
    (2, "IN PROGRESS"),
    (3, "CLOSED"),
)


class IsuesManager(models.Manager):
    def filter_by_participant(self, user: User):
        return self.filter(Q(junior=user) | Q(senior=user))


class Issue(TimestampMixin):
    title = models.CharField(max_length=50)
    status = models.PositiveSmallIntegerField(choices=ISSUE_STATUS_CGOICES)
    body = models.TextField(null=True)

    junior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="junior_issues"
    )
    senior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="senior_issues", null=True
    )

    objects = IsuesManager()

    # class Meta:
    #     schema = 'ds0903'

    def __repr__(self) -> str:
        return f"Issue[{self.pk} {self.title[:10]}]"

    def __str__(self) -> str:
        return self.title[:10]


class Message(models.Model):
    body: str = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
