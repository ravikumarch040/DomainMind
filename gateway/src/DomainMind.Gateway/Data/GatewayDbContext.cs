using Microsoft.EntityFrameworkCore;

namespace DomainMind.Gateway.Data;

public class GatewayDbContext : DbContext
{
    public GatewayDbContext(DbContextOptions<GatewayDbContext> options) : base(options) { }

    public DbSet<RequestLog> RequestLogs => Set<RequestLog>();
    public DbSet<ApiKey> ApiKeys => Set<ApiKey>();
    public DbSet<Conversation> Conversations => Set<Conversation>();
}

public class RequestLog
{
    public Guid Id { get; set; }
    public string TenantId { get; set; } = "";
    public string PromptTokenized { get; set; } = "";
    public string ResponseTokenized { get; set; } = "";
    public string ModelMode { get; set; } = "";
    public DateTime CreatedAt { get; set; }
}

public class ApiKey
{
    public Guid Id { get; set; }
    public string TenantId { get; set; } = "";
    public string KeyHash { get; set; } = "";
    public string Role { get; set; } = "Viewer";
    public bool IsActive { get; set; } = true;
}

public class Conversation
{
    public Guid Id { get; set; }
    public string TenantId { get; set; } = "";
    public string Title { get; set; } = "";
    public string MessagesJson { get; set; } = "[]";
    public DateTime UpdatedAt { get; set; }
}
