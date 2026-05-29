using DomainMind.Gateway.Services;

namespace DomainMind.Gateway.Middleware;

public class RbacMiddleware
{
    private static readonly HashSet<string> WriteRoles = new(StringComparer.OrdinalIgnoreCase)
        { "Admin", "Editor" };

    private readonly RequestDelegate _next;

    public RbacMiddleware(RequestDelegate next) => _next = next;

    public async Task InvokeAsync(HttpContext context, ITenantContext tenant)
    {
        if (context.Request.Path.StartsWithSegments("/admin") ||
            context.Request.Method is "POST" or "PUT" or "DELETE")
        {
            if (context.Request.Path.Value?.Contains("/v1/chat/completions") == true)
            {
                await _next(context);
                return;
            }
            if (!WriteRoles.Contains(tenant.Role) && context.Request.Path.StartsWithSegments("/admin"))
            {
                context.Response.StatusCode = StatusCodes.Status403Forbidden;
                await context.Response.WriteAsync("Insufficient permissions");
                return;
            }
        }
        await _next(context);
    }
}
