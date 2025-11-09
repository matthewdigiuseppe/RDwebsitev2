# AI Access Configuration Guide

This website is configured to allow AI crawlers and assistants to access its content.

## Files Added

1. **`.htaccess`** - For Apache servers (most shared hosting)
2. **`_headers`** - For Netlify, Cloudflare Pages, Vercel
3. **`netlify.toml`** - For Netlify-specific configuration

## If Still Getting 403 Errors

The 403 error blocking AI access is likely coming from your hosting provider or CDN. Here's how to fix it:

### For Cloudflare Users

1. Log into your Cloudflare dashboard
2. Go to **Security** → **WAF** (Web Application Firewall)
3. Check **Custom Rules** and **Rate Limiting Rules**
4. Add a rule to **Allow** traffic from AI user-agents:
   - Rule name: "Allow AI Crawlers"
   - Field: User Agent
   - Operator: contains
   - Value: `claudebot` OR `ChatGPT` OR `GPTBot` OR `anthropic`
   - Action: **Allow**

5. Go to **Security** → **Bots**
6. Make sure "AI Crawlers" category is set to **Allow**

### For Apache/cPanel Hosting

The `.htaccess` file should work automatically. If not:
1. Verify `.htaccess` is in your public_html or www root directory
2. Check that `mod_rewrite` and `mod_headers` are enabled
3. Contact your hosting provider to whitelist AI user-agents

### For Nginx

Create or edit your nginx configuration:

```nginx
# Allow AI crawlers
if ($http_user_agent ~* (claudebot|anthropic-ai|claude-web|ChatGPT|GPTBot|Google-Extended|Gemini|PerplexityBot)) {
    set $allow_ai 1;
}

location / {
    if ($allow_ai = 1) {
        # Allow access
    }
    try_files $uri $uri/ =404;
}
```

### For Netlify

The `netlify.toml` and `_headers` files should work automatically.

If still blocked:
1. Go to Netlify dashboard → Site settings → Build & deploy
2. Check "Post processing" settings
3. Disable any aggressive bot protection

### For Vercel

Create `vercel.json`:

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Robots-Tag",
          "value": "index, follow, all"
        }
      ]
    }
  ]
}
```

### For GitHub Pages

GitHub Pages doesn't block AI crawlers by default. If you're experiencing issues, it may be a temporary GitHub service issue.

## Testing AI Access

After deploying these changes, test with:

```bash
curl -A "claudebot" https://realdegrees.net
curl -A "ChatGPT-User" https://realdegrees.net
```

Both should return 200 status codes, not 403.

## Common AI User-Agents

This configuration whitelists:
- **Claude**: `claudebot`, `anthropic-ai`, `claude-web`
- **ChatGPT**: `ChatGPT-User`, `GPTBot`, `OAI-SearchBot`
- **Google AI**: `Google-Extended`, `Gemini`, `Bard`
- **Bing AI**: `bingbot`, `BingPreview`
- **Perplexity**: `PerplexityBot`

## Need More Help?

Check your hosting provider's documentation for "allowing specific user-agents" or "whitelist bots".
