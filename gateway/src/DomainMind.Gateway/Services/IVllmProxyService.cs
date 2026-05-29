namespace DomainMind.Gateway.Services;

public interface IVllmProxyService
{
    Task<HttpResponseMessage> ProxyChatCompletionAsync(
        HttpRequest request,
        string modelMode,
        CancellationToken ct = default);
}

public interface IRequestLogService
{
    Task LogAsync(string tenantId, string prompt, string response, string modelMode);
}

public interface ITenantContext
{
    string TenantId { get; }
    string Role { get; }
    void Set(string tenantId, string role);
}

public interface IRateLimitService
{
    Task<bool> AllowAsync(string tenantId, int limitPerMinute);
}
