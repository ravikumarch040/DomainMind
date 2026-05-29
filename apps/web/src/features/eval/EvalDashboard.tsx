import { useState } from "react";
import { useQuery } from "react-query";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { getEvalRun, runEval } from "../../lib/api";

const MOCK_TREND = [
  { version: "v0.1", faithfulness: 0.72, rouge: 0.45 },
  { version: "v0.2", faithfulness: 0.78, rouge: 0.52 },
  { version: "v0.3", faithfulness: 0.81, rouge: 0.58 },
];

export default function EvalDashboard() {
  const [runId, setRunId] = useState<string | null>(null);
  const [selectedQ, setSelectedQ] = useState(0);
  const [thumbs, setThumbs] = useState<Record<number, "up" | "down">>({});

  const { data: runData, refetch } = useQuery(
    ["eval", runId],
    () => (runId ? getEvalRun(runId) : null),
    { enabled: !!runId, refetchInterval: runId ? 3000 : false }
  );

  const startEval = async () => {
    const res = await runEval();
    setRunId(res.run_id);
    refetch();
  };

  const comparisonRows = [
    { system: "base", faithfulness: 0.65, rouge: 0.4, bert: 0.55 },
    { system: "fine_tuned", faithfulness: 0.74, rouge: 0.52, bert: 0.68 },
    { system: "rag", faithfulness: 0.78, rouge: 0.48, bert: 0.62 },
    { system: "combined", faithfulness: 0.85, rouge: 0.61, bert: 0.75 },
  ];

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Eval Dashboard</h2>
        <button onClick={startEval} className="bg-emerald-600 px-4 py-2 rounded-lg text-sm">
          Run new eval
        </button>
      </div>
      {runId && (
        <p className="text-sm text-slate-400">
          Run {runId}: {runData?.status ?? "polling..."}
        </p>
      )}
      <div className="overflow-x-auto">
        <table className="w-full text-sm border border-slate-800">
          <thead className="bg-slate-900">
            <tr>
              <th className="p-2 text-left">System</th>
              <th className="p-2">Faithfulness</th>
              <th className="p-2">ROUGE-L</th>
              <th className="p-2">BERTScore</th>
            </tr>
          </thead>
          <tbody>
            {comparisonRows.map((r) => (
              <tr key={r.system} className="border-t border-slate-800">
                <td className="p-2">{r.system}</td>
                <td className="p-2 text-center">{r.faithfulness.toFixed(2)}</td>
                <td className="p-2 text-center">{r.rouge.toFixed(2)}</td>
                <td className="p-2 text-center">{r.bert.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={MOCK_TREND}>
            <XAxis dataKey="version" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" domain={[0, 1]} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="faithfulness" stroke="#34d399" />
            <Line type="monotone" dataKey="rouge" stroke="#60a5fa" />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <h3 className="text-sm font-medium mb-2">Side-by-side (question {selectedQ + 1})</h3>
          {["base", "fine_tuned", "rag", "combined"].map((sys) => (
            <div key={sys} className="mb-2 p-2 bg-slate-900 rounded text-xs">
              <strong>{sys}:</strong> Sample answer for compliance question...
            </div>
          ))}
          <div className="flex gap-2 mt-2">
            <button onClick={() => setThumbs({ ...thumbs, [selectedQ]: "up" })}>👍</button>
            <button onClick={() => setThumbs({ ...thumbs, [selectedQ]: "down" })}>👎</button>
          </div>
        </div>
        <div>
          <button
            onClick={() => window.open("/evals/reports/latest.pdf")}
            className="text-sm text-emerald-400 underline"
          >
            Export PDF report
          </button>
        </div>
      </div>
    </div>
  );
}
