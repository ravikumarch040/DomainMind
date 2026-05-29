using Microsoft.Extensions.Options;

namespace DomainMind.Gateway.Services;

public class VllmProxyService : IVllmProxyService
{
    private readonly HttpClient _http;
    private readonly GatewayOptions _options;

    public VllmProxyService(HttpClient http, IOptions<GatewayOptions> options)
    {
        _http = http;
        _options = options.Value;
    }

    public async Task<HttpResponseMessage> ProxyChatCompletionAsync(
        HttpRequest request,
        string modelMode,
        CancellationToken ct = default)
    {
        var baseUrl = modelMode == "base"
            ? _options.VllmBaseModelUrl
            : _options.VllmBaseUrl;

        using var reader = new StreamReader(request.Body);
        var body = await reader.ReadToEndAsync(ct);

        var msg = new HttpRequestMessage(HttpMethod.Post, $"{baseUrl.TrimEnd('/')}/v1/chat/completions")
        {
            Content = new StringContent(body, System.Text.Encoding.UTF8, "application/json"),
        };

        return await _http.SendAsync(msg, HttpCompletionOption.ResponseHeadersRead, ct);
    }
}
