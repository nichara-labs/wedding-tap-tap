// biome-ignore lint/correctness/noUnusedVariables: cloudfront
function handler(event) {
  const request = event.request;

  /* Cloudfront strips url fragments and query strings from the uri
    https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/functions-event-structure.html#functions-event-structure-request */
  let uri = request.uri;

  if (uri === "/") return request;

  // Strip trailing slashes
  uri = uri.replace(/\/+$/, "");

  // If the last element of the path has no extension, append .html
  const isHtmlPage = /\/[\w-]+$/;
  if (isHtmlPage.test(uri)) {
    uri = `${uri}.html`;
  }

  request.uri = uri;

  return request;
}
