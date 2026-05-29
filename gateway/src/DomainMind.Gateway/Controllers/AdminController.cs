using DomainMind.Gateway.Data;
using DomainMind.Gateway.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace DomainMind.Gateway.Controllers;

[ApiController]
[Route("admin")]
[Authorize]
public class AdminController : ControllerBase
{
    private readonly GatewayDbContext _db;
    private readonly ITenantContext _tenant;

    public AdminController(GatewayDbContext db, ITenantContext tenant)
    {
        _db = db;
        _tenant = tenant;
    }

    [HttpGet("usage")]
    public async Task<IActionResult> Usage()
    {
        if (_tenant.Role != "Admin")
            return Forbid();

        var count = await _db.RequestLogs
            .Where(r => r.TenantId == _tenant.TenantId)
            .CountAsync();

        return Ok(new { tenant_id = _tenant.TenantId, queries = count });
    }

    [HttpPost("system-prompt")]
    public IActionResult SetSystemPrompt([FromBody] SystemPromptRequest req)
    {
        if (_tenant.Role is not "Admin" and not "Editor")
            return Forbid();
        return Ok(new { tenant_id = _tenant.TenantId, prompt = req.Prompt });
    }
}

public record SystemPromptRequest(string Prompt);
