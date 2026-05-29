namespace DomainMind.Gateway.Services;

public class TenantContext : ITenantContext
{
    public string TenantId { get; private set; } = "default";
    public string Role { get; private set; } = "Viewer";

    public void Set(string tenantId, string role)
    {
        TenantId = tenantId;
        Role = role;
    }
}
