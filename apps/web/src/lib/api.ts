const GATEWAY = import.meta.env.VITE_GATEWAY_URL || "/api";
const EVAL = import.meta.env.VITE_EVAL_URL || "/eval";
const ORCHESTRATOR = import.meta.env.VITE_ORCHESTRATOR_URL || "/orchestrator";

export type ModelMode = "base" | "fine_tuned" | "rag" | "combined";

export async function streamChat(
  query: string,
  modelMode: ModelMode,
  onToken: (token: string) => void,
  onCitations?: (citations: unknown[]) => void
): Promise<void> {
  const res = await fetch(`${ORCHESTRATOR}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, tenant_id: "default", model_mode: modelMode }),
  });
  const reader = res.body?.getReader();
  if (!reader) return;
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value);
    for (const line of chunk.split("\n")) {
      if (line.startsWith("data: ")) {
        try {
          const data = JSON.parse(line.slice(6));
          if (data.token) onToken(data.token);
          if (data.citations && onCitations) onCitations(data.citations);
        } catch { /* partial SSE */ }
      }
    }
  }
}

export async function runEval(runId?: string) {
  const res = await fetch(`${EVAL}/eval/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ run_id: runId }),
  });
  return res.json();
}

export async function getEvalRun(runId: string) {
  const res = await fetch(`${EVAL}/eval/runs/${runId}`);
  return res.json();
}

export async function uploadDocument(file: File, onProgress: (pct: number) => void) {
  onProgress(10);
  const form = new FormData();
  form.append("file", file);
  await new Promise((r) => setTimeout(r, 500));
  onProgress(50);
  await fetch(`${GATEWAY}/admin/index`, { method: "POST", body: form }).catch(() => {});
  onProgress(100);
}
