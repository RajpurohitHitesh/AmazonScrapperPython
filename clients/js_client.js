async function scrapeProduct({ baseUrl, apiKey, url }) {
  const resp = await fetch(`${baseUrl.replace(/\/$/, '')}/api/scrape`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': apiKey,
    },
    body: JSON.stringify({ url }),
  });
  if (!resp.ok) {
    throw new Error(`Request failed: ${resp.status}`);
  }
  return resp.json();
}

// Example
// scrapeProduct({ baseUrl: 'http://127.0.0.1:5000', apiKey: 'your_api_key_here', url: 'https://www.amazon.com/dp/B0FMDNZ61S' })
//   .then(console.log)
//   .catch(console.error);
