/*
For google tag gateway https://developers.google.com/tag-platform/tag-manager/gateway/setup-guide?setup=manual#other

Confirm geolocation is working with https://YOURDOMAIN.com/TAG_GATEWAY_PATH/?validate_geo=healthy
*/

// biome-ignore lint/correctness/noUnusedVariables: cloudfront
function handler(event) {
  const req = event.request;
  const h = req.headers;

  /* Available headers: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/adding-cloudfront-headers.html */
  const countryHeader = "cloudfront-viewer-country";
  const regionHeader = "cloudfront-viewer-country-region";
  const country = h[countryHeader]
    ? h[countryHeader].value
      ? h[countryHeader].value
      : ""
    : "";
  const region = h[regionHeader]
    ? h[regionHeader].value
      ? h[regionHeader].value
      : ""
    : "";

  /* Header structure: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/functions-event-structure.html#functions-event-structure-query-header-cookie */
  if (country && region) {
    h["x-forwarded-countryregion"] = { value: `${country}-${region}` };
  } else {
    if (country) h["x-forwarded-country"] = { value: country };
    if (region) {
      h["x-forwarded-region"] = { value: region };
    }
  }
  return req;
}
