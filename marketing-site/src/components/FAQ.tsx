import { useState } from "react";

interface FAQItem {
  q: string;
  a: string;
}

interface FAQProps {
  items: FAQItem[];
}

export default function FAQ({ items }: FAQProps) {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <div className="divide-y divide-marketing-border rounded-2xl border border-marketing-border bg-marketing-surface">
      {items.map((item, i) => (
        <div key={item.q}>
          <button
            type="button"
            onClick={() => setOpenIndex(openIndex === i ? null : i)}
            className="flex w-full items-center justify-between px-6 py-5 text-left"
            aria-expanded={openIndex === i}
          >
            <span className="pr-4 font-medium text-marketing-text">{item.q}</span>
            <span className="shrink-0 text-marketing-accent">{openIndex === i ? "−" : "+"}</span>
          </button>
          {openIndex === i && (
            <div className="px-6 pb-5 text-sm leading-relaxed text-marketing-muted">{item.a}</div>
          )}
        </div>
      ))}
    </div>
  );
}
