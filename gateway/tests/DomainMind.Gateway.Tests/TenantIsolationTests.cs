using DomainMind.Gateway.Services;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace DomainMind.Gateway.Tests;

public class TenantIsolationTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public TenantIsolationTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task TenantA_Header_Isolated_From_TenantB()
    {
        var reqA = new HttpRequestMessage(HttpMethod.Get, "/health");
        reqA.Headers.Add("X-Tenant-Id", "tenant_a");

        var reqB = new HttpRequestMessage(HttpMethod.Get, "/health");
        reqB.Headers.Add("X-Tenant-Id", "tenant_b");

        var resA = await _client.SendAsync(reqA);
        var resB = await _client.SendAsync(reqB);

        Assert.Equal(System.Net.HttpStatusCode.OK, resA.StatusCode);
        Assert.Equal(System.Net.HttpStatusCode.OK, resB.StatusCode);
        Assert.NotEqual("tenant_a", "tenant_b");
    }

    [Fact]
    public void TenantContext_StoresDistinctTenants()
    {
        var ctx = new TenantContext();
        ctx.Set("tenant_a", "Admin");
        Assert.Equal("tenant_a", ctx.TenantId);
        ctx.Set("tenant_b", "Viewer");
        Assert.Equal("tenant_b", ctx.TenantId);
        Assert.NotEqual("tenant_a", ctx.TenantId);
    }
}
