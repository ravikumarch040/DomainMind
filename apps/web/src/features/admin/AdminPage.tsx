import { useState } from "react";

export default function AdminPage() {
  const [systemPrompt, setSystemPrompt] = useState(
    "You are a compliance and legal expert specializing in SOC 2, HIPAA, and HITECH."
  );
  const [apiKeys] = useState([{ id: "1", prefix: "dm_live_••••", role: "Editor" }]);

  const savePrompt = async () => {
    await fetch("/api/admin/system-prompt", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Role": "Admin" },
      body: JSON.stringify({ prompt: systemPrompt }),
    });
  };

  return (
    <div className="space-y-8 max-w-2xl">
      <h2 className="text-xl font-semibold">Admin Panel</h2>
      <section>
        <h3 className="text-sm font-medium text-slate-400 mb-2">System prompt</h3>
        <textarea
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          rows={4}
          className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm"
        />
        <button onClick={savePrompt} className="mt-2 bg-emerald-600 px-4 py-2 rounded text-sm">
          Save
        </button>
      </section>
      <section>
        <h3 className="text-sm font-medium text-slate-400 mb-2">API keys</h3>
        <ul className="space-y-2">
          {apiKeys.map((k) => (
            <li key={k.id} className="bg-slate-900 p-3 rounded flex justify-between">
              <span>{k.prefix}</span>
              <span className="text-slate-500">{k.role}</span>
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h3 className="text-sm font-medium text-slate-400 mb-2">Tenant usage</h3>
        <p className="text-2xl font-mono">1,247 queries · 2.1M tokens</p>
      </section>
    </div>
  );
}
