import { demoMailto, hero, pillars } from "../content/site";
import ChatMock from "./mockups/ChatMock";

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-white to-marketing-bg pb-16 pt-12 md:pb-24 md:pt-16">
      <div
        className="pointer-events-none absolute inset-0 opacity-40"
        style={{
          backgroundImage: `radial-gradient(circle at 20% 50%, rgba(37, 99, 235, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(196, 169, 98, 0.1) 0%, transparent 40%)`,
        }}
      />

      <div className="relative mx-auto max-w-6xl px-6">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div className="fade-in">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-marketing-gold/30 bg-marketing-gold/10 px-3 py-1 text-xs font-medium text-marketing-gold">
              Built for compliance officers & risk teams
            </div>
            <h1 className="font-serif text-4xl leading-tight text-marketing-text md:text-5xl lg:text-[3.25rem]">
              {hero.headline}
            </h1>
            <p className="mt-6 text-lg leading-relaxed text-marketing-muted">{hero.subhead}</p>
            <div className="mt-8 flex flex-wrap gap-4">
              <a
                href={demoMailto}
                className="rounded-lg bg-marketing-accent px-6 py-3 font-semibold text-white transition hover:bg-blue-700"
              >
                {hero.primaryCta}
              </a>
              <a
                href="#how-it-works"
                className="rounded-lg border border-marketing-border bg-marketing-surface px-6 py-3 font-semibold text-marketing-text transition hover:border-marketing-accent hover:text-marketing-accent"
              >
                {hero.secondaryCta}
              </a>
            </div>

            <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-4">
              {pillars.map((p) => (
                <div key={p.label}>
                  <p className="text-sm font-semibold text-marketing-text">{p.label}</p>
                  <p className="mt-1 text-xs text-marketing-muted">{p.description}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="fade-in lg:pl-4">
            <ChatMock />
          </div>
        </div>
      </div>
    </section>
  );
}
