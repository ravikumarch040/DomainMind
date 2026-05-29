using DomainMind.Gateway.Services;
using Microsoft.Extensions.Options;

namespace DomainMind.Gateway.Middleware;

public class RateLimitMiddleware
{
    private readonly RequestDelegate _next;
    private readonly GatewayOptions _options;

    public RateLimitMiddleware(RequestDelegate next, IOptions<GatewayOptions> options)
    {
        _next = next;
        _options = options.Value;
    }

    public async Task InvokeAsync(HttpContext context, ITenantContext tenant, IRateLimitService rateLimit)
    {
        if (!await rateLimit.AllowAsync(tenant.TenantId, _options.RateLimitPerMinute))
        {
            context.Response.StatusCode = StatusCodes.Status429TooManyRequests;
            await context.Response.WriteAsync("Rate limit exceeded");
            return;
        }
        await _next(context);
    }
}
