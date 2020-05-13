# Simple Lambda Stopinator: Start/Stop EC2 instances on schedule or duration

Use these stopinators to start/stop Amazon EC2 instances based on rules defined in tags.

They are "Simple" because all code is in one text file, so it is easy to paste into a Lambda function. Just add an IAM Role and you're up and running!

There are multiple stopinators available in this repository.

## Stopinator Type 1: Auto-Stop

Run this AWS Lambda function on a **schedule** to auto-stop EC2 instances at night. A schedule can be specified via Amazon CloudWatch Events.

By default, all Amazon EC2 instances will be stopped.

Add an `Auto-Stop` tag to an instance to change this behaviour, with a Value of:
- `Stop` to stop the instance (same as default)
- `Terminate` to terminate the instance (good for temporary instances)
- `Ignore` to skip-over the instance (Don't stop it)

---

## Stopinator Type 2: Stop instances after given duration

- Will Stop any running Amazon EC2 instance with a `Stop-After` tag
- Will Terminate any running Amazon EC2 instance with a `Terminate-After` tag
- The tag Value indicates running duration (eg `30m`, `24h`)

Schedule this Lambda function to run at regular intervals (eg every 5 minutes) to check the instances.

---

## Stopinator Type 3: The Ultimate Stopinator!

This AWS Lambda function will **start and stop instances at given times and durations**.

It can also **notify** about instances left running.

Add a tag to instances:

- `sls-stop-after`: Stop instance after given duration
- `sls-terminate-after`: Terminate instance after given duration
- `sls-notify-after`: Notify about running instance after given duration
- `sls-last-checked`: Used by SLS to track previous notification times (internal use only)

- `sls-start-at`: The time of day to start an instance
- `sls-stop-at`: The time of day to stop an instance
- `sls-terminate-at`: The time of day to terminate an instance

Schedule this Lambda function to run at regular intervals (eg every 5 minutes)

(Still a work-in-progress)
