using DomainMind.Gateway.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace DomainMind.Gateway.Controllers;

[ApiController]
[Route("v1")]
public class ChatController : ControllerBase
{
    private readonly IVllmProxyService _proxy;

    public ChatController(IVllmProxyService proxy) => _proxy = proxy;

    [HttpPost("chat/completions")]
    [AllowAnonymous]
    public async Task<IActionResult> ChatCompletions(CancellationToken ct)
    {
        var modelMode = Request.Headers["X-Model-Mode"].FirstOrDefault() ?? "combined";

        if (!Request.Headers.ContainsKey("Authorization") &&
            !Request.Headers.ContainsKey("X-API-Key") &&
            !HttpContext.RequestServices.GetRequiredService<IWebHostEnvironment>().IsDevelopment())
        {
            return Unauthorized();
        }

        try
        {
            var response = await _proxy.ProxyChatCompletionAsync(Request, modelMode, ct);
            var content = await response.Content.ReadAsStringAsync(ct);
            return new ContentResult
            {
                Content = content,
                ContentType = "application/json",
                StatusCode = (int)response.StatusCode,
            };
        }
        catch (HttpRequestException)
        {
            return StatusCode(503, new
            {
                error = new { message = "vLLM service unavailable", type = "service_unavailable" },
            });
        }
    }
}
