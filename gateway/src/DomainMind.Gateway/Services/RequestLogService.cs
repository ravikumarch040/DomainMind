using DomainMind.Gateway.Data;
using System.Security.Cryptography;
using System.Text;

namespace DomainMind.Gateway.Services;

public class RequestLogService : IRequestLogService
{
    private readonly GatewayDbContext _db;

    public RequestLogService(GatewayDbContext db) => _db = db;

    public async Task LogAsync(string tenantId, string prompt, string response, string modelMode)
    {
        _db.RequestLogs.Add(new RequestLog
        {
            Id = Guid.NewGuid(),
            TenantId = tenantId,
            PromptTokenized = TokenizePhi(prompt),
            ResponseTokenized = TokenizePhi(response),
            ModelMode = modelMode,
            CreatedAt = DateTime.UtcNow,
        });
        await _db.SaveChangesAsync();
    }

    private static string TokenizePhi(string text)
    {
        if (string.IsNullOrEmpty(text)) return text;
        return Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(text)))[..16] + "...";
    }
}
