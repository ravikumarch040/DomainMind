using System.Text;
using DomainMind.Gateway.Services;

namespace DomainMind.Gateway.Middleware;

public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;

    public RequestLoggingMiddleware(RequestDelegate next) => _next = next;

    public async Task InvokeAsync(HttpContext context, ITenantContext tenant, IRequestLogService logger)
    {
        if (!context.Request.Path.StartsWithSegments("/v1/chat/completions"))
        {
            await _next(context);
            return;
        }

        context.Request.EnableBuffering();
        var prompt = await new StreamReader(context.Request.Body, Encoding.UTF8, leaveOpen: true).ReadToEndAsync();
        context.Request.Body.Position = 0;

        var originalBody = context.Response.Body;
        using var memStream = new MemoryStream();
        context.Response.Body = memStream;

        await _next(context);

        memStream.Position = 0;
        var response = await new StreamReader(memStream).ReadToEndAsync();
        memStream.Position = 0;
        await memStream.CopyToAsync(originalBody);

        var modelMode = context.Request.Headers["X-Model-Mode"].FirstOrDefault() ?? "combined";
        try
        {
            await logger.LogAsync(tenant.TenantId, prompt, response, modelMode);
        }
        catch { /* non-fatal */ }
    }
}
