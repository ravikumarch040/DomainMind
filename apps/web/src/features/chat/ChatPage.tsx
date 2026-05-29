import { useState } from "react";
import { ModelMode, streamChat } from "../../lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  citations?: { doc_name: string; chunk_id: string }[];
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [modelMode, setModelMode] = useState<ModelMode>("combined");
  const [streaming, setStreaming] = useState(false);

  const send = async () => {
    if (!input.trim() || streaming) return;
    const userMsg: Message = { role: "user", content: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setStreaming(true);
    let assistant = "";
    setMessages((m) => [...m, { role: "assistant", content: "" }]);

    await streamChat(
      userMsg.content,
      modelMode,
      (token) => {
        assistant += token;
        setMessages((m) => {
          const copy = [...m];
          copy[copy.length - 1] = { role: "assistant", content: assistant };
          return copy;
        });
      },
      (citations) => {
        setMessages((m) => {
          const copy = [...m];
          copy[copy.length - 1] = {
            role: "assistant",
            content: assistant,
            citations: citations as Message["citations"],
          };
          return copy;
        });
      }
    );
    setStreaming(false);
  };

  const copy = (text: string) => navigator.clipboard.writeText(text);

  return (
    <div className="flex flex-col h-[calc(100vh-3rem)]">
      <div className="flex gap-4 mb-4 items-center">
        <label className="text-sm text-slate-400">Model mode</label>
        <select
          value={modelMode}
          onChange={(e) => setModelMode(e.target.value as ModelMode)}
          className="bg-slate-800 border border-slate-700 rounded px-3 py-1"
        >
          <option value="base">Base LLM</option>
          <option value="fine_tuned">Fine-tuned</option>
          <option value="rag">RAG only</option>
          <option value="combined">Fine-tuned + RAG</option>
        </select>
      </div>
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-4 rounded-lg max-w-3xl ${msg.role === "user" ? "bg-slate-800 ml-auto" : "bg-slate-900"}`}
          >
            <p className="whitespace-pre-wrap">{msg.content}</p>
            {msg.citations && msg.citations.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {msg.citations.map((c, j) => (
                  <span key={j} className="text-xs bg-emerald-900/50 text-emerald-300 px-2 py-1 rounded">
                    {c.doc_name} · {c.chunk_id}
                  </span>
                ))}
              </div>
            )}
            {msg.role === "assistant" && msg.content && (
              <button onClick={() => copy(msg.content)} className="text-xs text-slate-500 mt-2 hover:text-slate-300">
                Copy
              </button>
            )}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Ask about SOC 2, HIPAA, HITECH..."
          className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-2"
          disabled={streaming}
        />
        <button
          onClick={send}
          disabled={streaming}
          className="bg-emerald-600 hover:bg-emerald-500 px-6 py-2 rounded-lg font-medium disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
