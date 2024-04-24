from django.db import models

from users.models import User

ISSUE_STATUS_CGOICES = (
    (1, "OPENED"),
    (2, "IN PROGRESS"),
    (3, "CLOSED"),
)


class Issue(models.Model):
    title = models.CharField(max_length=50)
    status = models.PositiveSmallIntegerField(choices=ISSUE_STATUS_CGOICES)
    body = models.TextField(null=True)

    junior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="junior_issues"
    )
    senior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="senior_issues", null=True
    )

    def __repr__(self) -> str:
        return f"Issue[{self.pk} {self.title[:10]}]"

    def __str__(self) -> str:
        return self.title[:10]


# instance: Issue = Issue.objects.get(id=1)

# issue.message_set


class Message(models.Model):
    body: str = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
