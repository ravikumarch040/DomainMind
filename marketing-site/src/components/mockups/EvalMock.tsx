import AppShellMock from "./AppShellMock";
import BrowserFrame from "./BrowserFrame";

const rows = [
  { system: "base", faithfulness: "0.65", rouge: "0.40", bert: "0.55" },
  { system: "fine_tuned", faithfulness: "0.74", rouge: "0.52", bert: "0.68" },
  { system: "rag", faithfulness: "0.78", rouge: "0.48", bert: "0.62" },
  { system: "combined", faithfulness: "0.85", rouge: "0.61", bert: "0.75" },
];

export default function EvalMock() {
  return (
    <BrowserFrame title="DomainMind — Eval">
      <AppShellMock active="Eval">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-semibold">Eval Dashboard</h2>
            <span className="rounded-lg bg-emerald-600 px-3 py-1.5 text-[10px]">Run new eval</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full border border-slate-800 text-[10px]">
              <thead className="bg-slate-900">
                <tr>
                  <th className="p-2 text-left">System</th>
                  <th className="p-2">Faithfulness</th>
                  <th className="p-2">ROUGE-L</th>
                  <th className="p-2">BERTScore</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.system} className="border-t border-slate-800">
                    <td className="p-2">{r.system}</td>
                    <td className="p-2 text-center">{r.faithfulness}</td>
                    <td className="p-2 text-center">{r.rouge}</td>
                    <td className="p-2 text-center">{r.bert}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="flex h-24 items-end gap-1 rounded bg-slate-900/50 p-3">
            {[0.72, 0.78, 0.81].map((v, i) => (
              <div key={i} className="flex flex-1 flex-col items-center gap-1">
                <div className="w-full rounded-t bg-emerald-500/80" style={{ height: `${v * 100}%` }} />
                <span className="text-[9px] text-slate-500">v0.{i + 1}</span>
              </div>
            ))}
          </div>
        </div>
      </AppShellMock>
    </BrowserFrame>
  );
}
