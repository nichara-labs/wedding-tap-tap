terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.5"
    }
  }
  required_version = "~> 1.10"
}

locals {
  s3_origin_id       = "S3 Bucket"
  s3_404_origin_id   = "S3 Website Endpoint for 404"
  s3_origin_group_id = "S3 Origin Group"
  backend_origin_id  = "Backend"
}

data "aws_cloudfront_cache_policy" "optimized" {
  name = "Managed-CachingOptimized"
}

data "aws_cloudfront_cache_policy" "disabled" {
  name = "Managed-CachingDisabled"
}

data "aws_cloudfront_origin_request_policy" "all_viewer" {
  # Required for App Runner to route requests correctly
  name = "Managed-AllViewerExceptHostHeader"
}

data "aws_cloudfront_response_headers_policy" "cors_security" {
  name = "Managed-CORS-and-SecurityHeadersPolicy"
}

resource "aws_cloudfront_origin_access_control" "s3" {
  name                              = "oac-${var.name}"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "cdn" {
  enabled             = true
  is_ipv6_enabled     = true
  http_version        = "http2and3"
  default_root_object = "index.html"
  aliases             = var.aliases
  wait_for_deployment = false


  # Frontend in S3 bucket
  origin {
    domain_name              = aws_s3_bucket.site.bucket_regional_domain_name
    origin_id                = local.s3_origin_id
    origin_access_control_id = aws_cloudfront_origin_access_control.s3.id
  }

  # Frontend S3 Website bucket, for 404 page fallback
  # Workaround Cloud Functions not running on 4xx errors
  # Compared to Lambda@Edge, this preserves the URL in the user's browser,
  # while showing the 404 page
  origin {
    domain_name = aws_s3_bucket_website_configuration.site_404.website_endpoint
    origin_id   = local.s3_404_origin_id

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  origin_group {
    origin_id = local.s3_origin_group_id
    failover_criteria {
      status_codes = [404]
    }
    member {
      origin_id = local.s3_origin_id
    }
    member {
      origin_id = local.s3_404_origin_id
    }
  }

  # Backend API
  origin {
    domain_name = var.domain_name
    origin_id   = local.backend_origin_id

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  viewer_certificate {
    acm_certificate_arn      = var.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  # Used for the frontend routes (*)
  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true
    target_origin_id       = local.s3_origin_group_id
    viewer_protocol_policy = "redirect-to-https"

    # Cache everything
    cache_policy_id = data.aws_cloudfront_cache_policy.optimized.id

    response_headers_policy_id = data.aws_cloudfront_response_headers_policy.cors_security.id

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.add_html_extension.arn
    }

  }

  # For backend: don't cache anything
  ordered_cache_behavior {
    path_pattern           = var.backend_path_pattern
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods         = ["GET", "HEAD", "OPTIONS"]
    compress               = true
    target_origin_id       = local.backend_origin_id
    viewer_protocol_policy = "redirect-to-https"

    # Forward all request headers to the origin
    origin_request_policy_id = data.aws_cloudfront_origin_request_policy.all_viewer.id

    # Don't cache anything
    cache_policy_id = data.aws_cloudfront_cache_policy.disabled.id
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Name = var.name
  }
}

resource "aws_cloudfront_function" "add_html_extension" {
  name    = "add_html_extension-${var.name}"
  runtime = "cloudfront-js-2.0"
  comment = "Adds .html extension to requests for HTML pages"
  publish = true
  code    = file("${path.module}/add_html_extension.js")
}

resource "aws_cloudfront_function" "add_geolocation" {
  name    = "add_geolocation-${var.name}"
  runtime = "cloudfront-js-2.0"
  comment = "Adds geolocation headers to requests, for Google Tag Gateway"
  publish = true
  code    = file("${path.module}/add_geolocation.js")
}
