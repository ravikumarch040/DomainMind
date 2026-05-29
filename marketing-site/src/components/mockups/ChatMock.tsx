import AppShellMock from "./AppShellMock";
import BrowserFrame from "./BrowserFrame";

export default function ChatMock() {
  return (
    <BrowserFrame title="DomainMind — Chat">
      <AppShellMock active="Chat">
        <div className="flex h-full flex-col">
          <div className="mb-3 flex items-center gap-3">
            <label className="text-xs text-slate-400">Model mode</label>
            <select className="rounded border border-slate-700 bg-slate-800 px-2 py-1 text-xs" defaultValue="combined">
              <option value="base">Base LLM</option>
              <option value="fine_tuned">Fine-tuned</option>
              <option value="rag">RAG only</option>
              <option value="combined">Fine-tuned + RAG</option>
            </select>
          </div>

          <div className="flex-1 space-y-3 overflow-hidden">
            <div className="ml-auto max-w-[85%] rounded-lg bg-slate-800 p-3 text-xs leading-relaxed">
              What are our HIPAA breach notification requirements?
            </div>
            <div className="max-w-[90%] rounded-lg bg-slate-900 p-3 text-xs leading-relaxed">
              <p>
                Per your policy, you must notify affected individuals within 60 days of discovering a breach.
                You must also notify HHS if the breach affects 500 or more individuals, and document all
                notifications in your breach log.
              </p>
              <div className="mt-2 flex flex-wrap gap-1.5">
                <span className="rounded bg-emerald-900/50 px-2 py-0.5 text-[10px] text-emerald-300">
                  hipaa-policy.pdf · chunk_12
                </span>
                <span className="rounded bg-emerald-900/50 px-2 py-0.5 text-[10px] text-emerald-300">
                  breach-procedure.docx · chunk_3
                </span>
              </div>
              <button type="button" className="mt-2 text-[10px] text-slate-500">
                Copy
              </button>
            </div>
          </div>

          <div className="mt-3 flex gap-2">
            <input
              readOnly
              value=""
              placeholder="Ask about SOC 2, HIPAA, HITECH..."
              className="flex-1 rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-xs placeholder:text-slate-500"
            />
            <button type="button" className="rounded-lg bg-emerald-600 px-4 py-2 text-xs font-medium">
              Send
            </button>
          </div>
        </div>
      </AppShellMock>
    </BrowserFrame>
  );
}
