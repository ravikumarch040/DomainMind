using System.Security.Claims;
using DomainMind.Gateway.Services;

namespace DomainMind.Gateway.Middleware;

public class TenantMiddleware
{
    private readonly RequestDelegate _next;

    public TenantMiddleware(RequestDelegate next) => _next = next;

    public async Task InvokeAsync(HttpContext context, ITenantContext tenant)
    {
        var tenantId = context.User.FindFirstValue("tenant_id")
            ?? context.Request.Headers["X-Tenant-Id"].FirstOrDefault()
            ?? "default";
        var role = context.User.FindFirstValue(ClaimTypes.Role)
            ?? context.Request.Headers["X-Role"].FirstOrDefault()
            ?? "Viewer";
        tenant.Set(tenantId, role);
        await _next(context);
    }
}
