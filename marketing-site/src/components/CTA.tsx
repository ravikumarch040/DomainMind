import { demoMailto } from "../content/site";

interface CTAProps {
  title: string;
  description?: string;
  button: string;
  compact?: boolean;
}

export default function CTA({ title, description, button, compact }: CTAProps) {
  return (
    <div className={`text-center ${compact ? "" : "max-w-2xl mx-auto"}`}>
      <h2 className="font-serif text-3xl md:text-4xl text-white">{title}</h2>
      {description && <p className="mt-4 text-lg text-slate-300">{description}</p>}
      <a
        href={demoMailto}
        className="mt-8 inline-block rounded-lg bg-marketing-accent px-8 py-3 font-semibold text-white transition hover:bg-blue-700"
      >
        {button}
      </a>
    </div>
  );
}
