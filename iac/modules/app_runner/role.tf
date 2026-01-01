# For the instance to access AWS services
resource "aws_iam_role" "instance_role" {
  name_prefix        = "${var.service_name}-app-runner-"
  assume_role_policy = data.aws_iam_policy_document.instance_assume_role.json
}

data "aws_iam_policy_document" "instance_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["tasks.apprunner.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "user_inline" {
  for_each = var.inline_policies

  name_prefix = "${each.key}-"
  role        = aws_iam_role.instance_role.id
  policy      = data.aws_iam_policy_document.user_inline[each.key].json
}

data "aws_iam_policy_document" "user_inline" {
  for_each = var.inline_policies

  dynamic "statement" {
    for_each = each.value
    content {
      effect    = statement.value.effect
      actions   = statement.value.actions
      resources = statement.value.resources
    }
  }
}

resource "aws_iam_role_policy_attachment" "user_managed" { # AWS Managed Policies
  for_each = var.managed_policies

  role       = aws_iam_role.instance_role.id
  policy_arn = each.key
}

# For App Runner to access ECR
resource "aws_iam_role" "service" {
  name_prefix        = "${var.service_name}-app-runner-"
  assume_role_policy = data.aws_iam_policy_document.service_assume_role.json
}

data "aws_iam_policy_document" "service_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["build.apprunner.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "app_runner" {
  role       = aws_iam_role.service.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}
