from issues.models import Issue


def main():
    issues = Issue.objects.all()
    print(issues)
    pass

if __name__ == "__name__"
    main()