namespace DomainMind.Gateway;

public class GatewayOptions
{
    public string VllmBaseUrl { get; set; } = "http://localhost:8000";
    public string VllmBaseModelUrl { get; set; } = "http://localhost:8000";
    public int RateLimitPerMinute { get; set; } = 60;
    public Dictionary<string, string> ApiKeys { get; set; } = new();
}
