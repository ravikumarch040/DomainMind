using Microsoft.Extensions.Options;
using StackExchange.Redis;

namespace DomainMind.Gateway.Services;

public class RedisRateLimitService : IRateLimitService
{
    private readonly IConnectionMultiplexer? _redis;
    private readonly GatewayOptions _options;

    public RedisRateLimitService(IOptions<GatewayOptions> options, IConfiguration config)
    {
        _options = options.Value;
        var redisUrl = config["Redis:ConnectionString"];
        if (!string.IsNullOrEmpty(redisUrl))
        {
            try { _redis = ConnectionMultiplexer.Connect(redisUrl); }
            catch { _redis = null; }
        }
    }

    public async Task<bool> AllowAsync(string tenantId, int limitPerMinute)
    {
        if (_redis is null) return true;

        var db = _redis.GetDatabase();
        var key = $"ratelimit:{tenantId}:{DateTime.UtcNow:yyyyMMddHHmm}";
        var count = await db.StringIncrementAsync(key);
        if (count == 1)
            await db.KeyExpireAsync(key, TimeSpan.FromMinutes(2));
        return count <= limitPerMinute;
    }
}
