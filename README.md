# Simple Lambda Stopinator: Start/Stop EC2 instances on schedule or duration

Use these stopinators to start/stop Amazon EC2 instances based on rules defined in tags.

They are "Simple" because all code is in one text file, so it is easy to paste into a Lambda function. Just add an IAM Role and you're up and running!

There are multiple stopinators available in this repository.

For details of how they work, see this blog post: [Simple EC2 Stopinator in Lambda - DEV Community](https://dev.to/aws/simple-ec2-stopinator-in-lambda-5goj)

---

## Stopinator Type 1: Auto-Stop

Run this AWS Lambda function on a **schedule** to auto-stop EC2 instances at night. A schedule can be specified via Amazon CloudWatch Events.

By default, all Amazon EC2 instances will be stopped.

Add an `Auto-Stop` tag to an instance to change this behaviour, with a Value of:
- `Stop` to stop the instance (same as default)
- `Terminate` to terminate the instance (good for temporary instances)
- `Ignore` to skip-over the instance (Don't stop it)

---

## Stopinator Type 2: Stop/Terminate/Notify instances after given duration

Use this stopinator to stop/terminate instances after they have been running for a given duration.

It can also send reminder notifications to an Amazon SNS topic at various durations.

**Tag Names** (in priority order):
- 'Terminate-After': Terminate instance
- 'Stop-After': Stop instance
- 'Notify-After': Send SNS notification if still running
  (For multiple notifications, use 'Notify-After1', 'Notify-After2', etc)

**Tag Value:** Indicates running duration (eg '30m', '1.5h', 24h')

Schedule this Lambda function to run at regular intervals (eg every 5 minutes) using Amazon CloudWatch Events.
