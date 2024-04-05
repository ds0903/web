from django.db import models

from users.models import User


class Issue(models.Model):
    title = models.CharField(max_length=50)
    status = models.PositiveSmallIntegerField()

    junior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="junior_issues"
    )
    senior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="senior_issues", null=True
    )


# instance: Issue = Issue.objects.get(id=1)

# issue.message_set


class Message(models.Model):
    body: str = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
